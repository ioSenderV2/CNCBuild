<#
.SYNOPSIS
  Build the printable documents - build-document.pdf, design-record.pdf and
  machine/drawings/shop-pack.pdf.

.DESCRIPTION
  Two steps: tools/md2html.py renders both HTML files at the repo root, then
  headless Edge prints each to PDF.

    build-document.pdf   machine/assembly.md       HOW TO BUILD IT. Parts, hardware,
                                                   what bolts to what, in order. This is
                                                   the one that goes to the machine.
    CNC Build.zip        four files in drawings/    WHAT GETS SENT OUT. Built after the
                                                   pack prints - see tools/make-bundle.ps1.
    design-record.pdf    the thirteen machine/*.md  WHY IT IS THAT SHAPE. The reasoning,
                                                   the options weighed, the figures that
                                                   moved. Reference, not a work document.

  EVERY OUTPUT IS DERIVED, NEVER AUTHORITATIVE. If a PDF and a .md file disagree,
  the .md file wins and the PDF is stale. Regenerate rather than edit.

  The Edge invocation is lifted from ioSender's tools/regen-overview-pdf.ps1,
  which already paid for two gotchas:

    * a FRESH --user-data-dir every run. Without it Edge attaches to the
      already-running instance and the print silently no-ops, leaving the old
      PDF in place with no error;
    * Edge prints ASYNCHRONOUSLY and can flush the file several seconds after
      the command returns, so POLL for the timestamp to advance. A fixed sleep
      raced and reported a false no-op while Edge was still writing.

  The HTML must stay at the REPO ROOT. Edge resolves relative hrefs against the
  HTML's own location at print time and writes the result into the PDF as an
  absolute file:/// URL, so machine/photos/*.jpg and the shop-pack links only
  point at real files from there.

.PARAMETER Doc
  Which document to build: build, record, pack, or all (the default).

.PARAMETER KeepHtml
  Leave the HTML files in place. They are kept by default; this switch exists so
  -KeepHtml:$false can delete them.

.EXAMPLE
  tools\make-pdf.ps1

.EXAMPLE
  tools\make-pdf.ps1 -Doc build
#>
[CmdletBinding()]
param(
    [ValidateSet('build', 'record', 'pack', 'dxf', 'all', 'both')]
    [string] $Doc = 'all',
    [switch] $KeepHtml = $true
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot

$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path $edge)) { Write-Host "ERROR: Edge not found at $edge" -ForegroundColor Red; exit 1 }

# The names here must match DOCS in tools/md2html.py.
$docs = @(
    [pscustomobject]@{ Key = 'build';  Html = 'build-document.html'; Pdf = 'build-document.pdf' }
    [pscustomobject]@{ Key = 'record'; Html = 'design-record.html';  Pdf = 'design-record.pdf'  }
    [pscustomobject]@{ Key = 'pack';   Html = 'machine/drawings/shop-pack.html'
                                       Pdf  = 'machine/drawings/shop-pack.pdf' }
    # The quote DXFs drawn back from their own bytes - what the shop receives.
    # THREE REQUESTS, QUOTED SEPARATELY, so three PDFs. They share the key so
    # -Doc dxf still means all of them and the generator still runs once.
    [pscustomobject]@{ Key = 'dxf';    Html = 'machine/drawings/dxf/quote-1-steel.html'
                                       Pdf  = 'machine/drawings/dxf/quote-1-steel.pdf' }
    [pscustomobject]@{ Key = 'dxf';    Html = 'machine/drawings/dxf/quote-2-x-back-joiner.html'
                                       Pdf  = 'machine/drawings/dxf/quote-2-x-back-joiner.pdf' }
    [pscustomobject]@{ Key = 'dxf';    Html = 'machine/drawings/dxf/quote-3-aluminium.html'
                                       Pdf  = 'machine/drawings/dxf/quote-3-aluminium.pdf' }
)
# 'both' still means the two root documents, so an older command line keeps working
if ($Doc -eq 'both') { $docs = $docs | Where-Object Key -in 'build', 'record' }
elseif ($Doc -ne 'all') { $docs = $docs | Where-Object Key -eq $Doc }

function Invoke-EdgePrint {
    param([string] $HtmlPath, [string] $PdfPath, [string] $Label)

    $before = if (Test-Path $PdfPath) { (Get-Item $PdfPath).LastWriteTime } else { [datetime]::MinValue }

    # Unique profile dir per run - the whole point. See the note at the top.
    $profileDir = Join-Path $env:TEMP ("edgepdf_" + [guid]::NewGuid().ToString('N'))
    $htmlUri = 'file:///' + ($HtmlPath -replace '\\', '/')

    Write-Host "Printing $Label ..." -ForegroundColor Cyan
    & $edge --headless=new --disable-gpu --no-pdf-header-footer `
        "--user-data-dir=$profileDir" "--print-to-pdf=$PdfPath" $htmlUri

    # Poll for the write to land rather than trusting a fixed wait.
    $deadline = (Get-Date).AddSeconds(90)
    do {
        Start-Sleep -Milliseconds 500
        $after = if (Test-Path $PdfPath) { (Get-Item $PdfPath).LastWriteTime } else { [datetime]::MinValue }
    } while ($after -le $before -and (Get-Date) -lt $deadline)

    if ($after -le $before) {
        Write-Host "ERROR: $Label did not change - Edge printed nothing. A stale instance attached" -ForegroundColor Red
        Write-Host "       despite the fresh profile dir, or the HTML failed to load." -ForegroundColor Red
        Remove-Item $profileDir -Recurse -Force -ErrorAction SilentlyContinue
        return -1
    }

    # Size can still settle for a moment after the first write - 16 photographs go in.
    $size = -1
    do {
        $prev = $size
        Start-Sleep -Milliseconds 700
        $size = (Get-Item $PdfPath).Length
    } while ($size -ne $prev)

    Remove-Item $profileDir -Recurse -Force -ErrorAction SilentlyContinue
    return $size
}

# --- 1. markdown -> HTML, both generated documents in one pass --------------------------
# The shop pack is hand-authored HTML and is not touched by this step.
if ($docs | Where-Object Key -eq 'dxf') {
    Write-Host "Drawing the quote DXFs back from their own bytes ..." -ForegroundColor Cyan
    & python (Join-Path $PSScriptRoot 'dxf-preview.py')
    if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: dxf-preview.py failed" -ForegroundColor Red; exit 1 }
    # The offsets printed on each page, checked back against the holes.
    & python (Join-Path $PSScriptRoot 'check-dxf-offsets.py')
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: a printed offset is not a hole centre - do not send these" -ForegroundColor Red
        exit 1
    }
}

if ($docs | Where-Object Key -in 'build', 'record') {
    Write-Host "Rendering from machine/*.md ..." -ForegroundColor Cyan
    & python (Join-Path $PSScriptRoot 'md2html.py')
    if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: md2html.py failed" -ForegroundColor Red; exit 1 }
}

# The pack's own two checks, so a stale tally or an untagged hole cannot reach the shop.
if ($docs | Where-Object Key -eq 'pack') {
    Write-Host "Rebuilding the hole tally and checking the pack ..." -ForegroundColor Cyan
    & python (Join-Path $PSScriptRoot 'build-hole-tally.py')
    if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: build-hole-tally.py failed" -ForegroundColor Red; exit 1 }
    & python (Join-Path $PSScriptRoot 'check-shop-pack-refs.py')
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: the shop pack fails its own checks - fix those before printing" -ForegroundColor Red
        exit 1
    }
}

# --- 2. HTML -> PDF via headless Edge ---------------------------------------------------
$failed = 0
foreach ($d in $docs) {
    $htmlPath = Join-Path $repo $d.Html
    $pdfPath = Join-Path $repo $d.Pdf
    if (-not (Test-Path $htmlPath)) {
        Write-Host "ERROR: $htmlPath not written" -ForegroundColor Red
        $failed++
        continue
    }

    # THE PACK IS HAND-AUTHORED AND PRINTS DIRECTLY, so it never passed through
    # tools/subst.py the way md2html runs the prose through it. It is printed
    # from a substituted copy instead - written BESIDE it so Edge resolves any
    # relative path the same way - which is what lets the pack cite a registry
    # symbol without the braces reaching paper.
    $printPath = $htmlPath
    $temp = $null
    if ($d.Key -eq 'pack') {
        $temp = Join-Path (Split-Path $htmlPath) 'shop-pack.print.html'
        & python (Join-Path $PSScriptRoot 'subst.py') '--render' $htmlPath $temp
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: the pack has an unknown symbol" -ForegroundColor Red
            $failed++
            continue
        }
        $printPath = $temp
    }

    $size = Invoke-EdgePrint -HtmlPath $printPath -PdfPath $pdfPath -Label $d.Pdf
    if ($temp -and (Test-Path $temp)) { Remove-Item $temp -Force }
    if ($size -lt 0) { $failed++; continue }

    if (-not $KeepHtml -and $d.Key -ne 'pack') { Remove-Item $htmlPath -Force }   # the pack's HTML is a source file
    $mb = [math]::Round($size / 1MB, 1)
    Write-Host "OK  $($d.Pdf)  $mb MB  ($size bytes)" -ForegroundColor Green
}

Write-Host "    Derived, never authoritative - if one disagrees with a .md file, the .md file wins." -ForegroundColor DarkGray

# --- 3. the send-out bundle -------------------------------------------------------------
# It carries shop-pack.pdf, so it is rebuilt whenever that is - a bundle holding
# last week's pack is the stale-copy failure this repo generates STATUS.md to avoid.
# Only on a clean print: zipping a PDF that failed to write would ship the old one.
if (-not $failed -and ($docs | Where-Object Key -eq 'pack')) {
    Write-Host "Bundling the send-out zip ..." -ForegroundColor Cyan
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'make-bundle.ps1')
    if ($LASTEXITCODE -ne 0) { $failed++ }
}

if ($failed) { exit 1 }
exit 0
