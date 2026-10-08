<#
.SYNOPSIS
  Build the two printable documents - build-document.pdf and design-record.pdf.

.DESCRIPTION
  Two steps: tools/md2html.py renders both HTML files at the repo root, then
  headless Edge prints each to PDF.

    build-document.pdf   machine/assembly.md       HOW TO BUILD IT. Parts, hardware,
                                                   what bolts to what, in order. This is
                                                   the one that goes to the machine.
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
  Which document to build: build, record, or both (the default).

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
    [ValidateSet('build', 'record', 'both')]
    [string] $Doc = 'both',
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
)
if ($Doc -ne 'both') { $docs = $docs | Where-Object Key -eq $Doc }

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

# --- 1. markdown -> HTML, both documents in one pass ------------------------------------
Write-Host "Rendering from machine/*.md ..." -ForegroundColor Cyan
& python (Join-Path $PSScriptRoot 'md2html.py')
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: md2html.py failed" -ForegroundColor Red; exit 1 }

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

    $size = Invoke-EdgePrint -HtmlPath $htmlPath -PdfPath $pdfPath -Label $d.Pdf
    if ($size -lt 0) { $failed++; continue }

    if (-not $KeepHtml) { Remove-Item $htmlPath -Force }
    $mb = [math]::Round($size / 1MB, 1)
    Write-Host "OK  $($d.Pdf)  $mb MB  ($size bytes)" -ForegroundColor Green
}

Write-Host "    Derived, never authoritative - if one disagrees with a .md file, the .md file wins." -ForegroundColor DarkGray
if ($failed) { exit 1 }
exit 0
