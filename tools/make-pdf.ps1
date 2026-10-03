<#
.SYNOPSIS
  Build build-document.pdf - the whole mechanical design as one printable file.

.DESCRIPTION
  Two steps: tools/md2html.py renders the twelve machine/*.md files into
  build-document.html at the repo root, then headless Edge prints that to
  build-document.pdf.

  BOTH OUTPUTS ARE DERIVED, NEVER AUTHORITATIVE. If the PDF and a .md file
  disagree, the .md file wins and the PDF is stale. Regenerate rather than edit.

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

.PARAMETER KeepHtml
  Leave build-document.html in place. It is kept by default; this switch exists
  so -KeepHtml:$false can delete it.

.EXAMPLE
  tools\make-pdf.ps1
#>
[CmdletBinding()]
param(
    [string] $Html = 'build-document.html',
    [string] $Pdf  = 'build-document.pdf',
    [switch] $KeepHtml = $true
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$htmlPath = Join-Path $repo $Html
$pdfPath  = Join-Path $repo $Pdf

# --- 1. markdown -> one HTML file -------------------------------------------------------
Write-Host "Rendering $($Html) from machine/*.md ..." -ForegroundColor Cyan
& python (Join-Path $PSScriptRoot 'md2html.py')
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: md2html.py failed" -ForegroundColor Red; exit 1 }
if (-not (Test-Path $htmlPath)) { Write-Host "ERROR: $htmlPath not written" -ForegroundColor Red; exit 1 }

# --- 2. HTML -> PDF via headless Edge ---------------------------------------------------
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path $edge)) { Write-Host "ERROR: Edge not found at $edge" -ForegroundColor Red; exit 1 }

$before = if (Test-Path $pdfPath) { (Get-Item $pdfPath).LastWriteTime } else { [datetime]::MinValue }

# Unique profile dir per run - the whole point. See the note above.
$profileDir = Join-Path $env:TEMP ("edgepdf_" + [guid]::NewGuid().ToString('N'))
$htmlUri = 'file:///' + ($htmlPath -replace '\\','/')

Write-Host "Printing $Html -> $Pdf ..." -ForegroundColor Cyan
& $edge --headless=new --disable-gpu --no-pdf-header-footer `
    "--user-data-dir=$profileDir" "--print-to-pdf=$pdfPath" $htmlUri

# Poll for the write to land rather than trusting a fixed wait.
$deadline = (Get-Date).AddSeconds(90)
do {
    Start-Sleep -Milliseconds 500
    $after = if (Test-Path $pdfPath) { (Get-Item $pdfPath).LastWriteTime } else { [datetime]::MinValue }
} while ($after -le $before -and (Get-Date) -lt $deadline)

if ($after -le $before) {
    Write-Host "ERROR: $Pdf did not change - Edge printed nothing. A stale instance attached" -ForegroundColor Red
    Write-Host "       despite the fresh profile dir, or the HTML failed to load." -ForegroundColor Red
    exit 1
}

# Size can still settle for a moment after the first write - 15 photographs go in.
$size = -1
do {
    $prev = $size
    Start-Sleep -Milliseconds 700
    $size = (Get-Item $pdfPath).Length
} while ($size -ne $prev)

Remove-Item $profileDir -Recurse -Force -ErrorAction SilentlyContinue
if (-not $KeepHtml) { Remove-Item $htmlPath -Force }

$mb = [math]::Round($size / 1MB, 1)
Write-Host "OK  $Pdf  $mb MB  ($size bytes)" -ForegroundColor Green
Write-Host "    Derived, never authoritative - if it disagrees with a .md file, the .md file wins." -ForegroundColor DarkGray
exit 0
