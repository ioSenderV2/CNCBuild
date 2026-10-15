<#
.SYNOPSIS
  Build machine/drawings/"CNC Build.zip" - the four files that get sent out.

.DESCRIPTION
  One attachment instead of four, for the machining visit and for anyone who
  asks what this machine is. What goes in:

    Interactive_Model.html   the 3D model. Self-contained - three.js is inlined,
                             so it opens from the unzipped folder with no server
                             and nothing to install
    shop-pack.pdf            what to make. The plate sheets, hole schedules and
                             per-sheet totals
    fasteners.html           what to buy and what goes where, with the totals by
                             thread size
    torsion-box-construction.html
                             the whole build of the torsion box - parts, sheets,
                             notches, sand ports and the glue-up order

  NOTHING HERE IS A SOURCE FILE. Every member is derived or tracked elsewhere,
  the zip itself is gitignored, and it is rebuilt rather than edited.

  THE NAMES INSIDE THE ZIP ARE THE NAMES ON DISK. A file that arrives as
  Shop-Pack.pdf and lives as shop-pack.pdf is one file with two names, and the
  second one is the one that cannot be grepped for.

  IT REFUSES RATHER THAN SHIPPING A SHORT ZIP. A missing member is the failure
  that does not announce itself: the zip builds, the mail goes, and the person
  at the other end finds three files where the mail said four. So every member
  is checked first and the whole thing stops if one is absent.

.PARAMETER Out
  Where to write it. Defaults to machine/drawings/CNC Build.zip.
#>
[CmdletBinding()]
param(
    [string] $Out
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$drawings = Join-Path $repo 'machine\drawings'
if (-not $Out) { $Out = Join-Path $drawings 'CNC Build.zip' }

# Relative to machine/drawings, in the order they are listed above.
$members = @(
    'Interactive_Model.html'
    'shop-pack.pdf'
    'fasteners.html'
    'torsion-box-construction.html'
)

$paths = @()
$absent = @()
foreach ($m in $members) {
    $p = Join-Path $drawings $m
    if (Test-Path -LiteralPath $p) { $paths += $p } else { $absent += $m }
}
if ($absent.Count) {
    Write-Host "ERROR: not in machine\drawings, so the zip would be short: $($absent -join ', ')" -ForegroundColor Red
    Write-Host "  shop-pack.pdf comes from tools\make-pdf.ps1 -Doc pack" -ForegroundColor DarkGray
    Write-Host "  fasteners.html comes from tools\make-fasteners.py" -ForegroundColor DarkGray
    exit 1
}

# Compress-Archive overwrites with -Force, but a stale zip left behind by a
# failed run would otherwise be indistinguishable from a fresh one.
if (Test-Path -LiteralPath $Out) { Remove-Item -LiteralPath $Out -Force }
Compress-Archive -LiteralPath $paths -DestinationPath $Out -CompressionLevel Optimal

$zip = Get-Item -LiteralPath $Out
Write-Host ("OK  {0}  {1:N1} MB  ({2} files)" -f
            $zip.FullName.Substring($repo.Length + 1),
            ($zip.Length / 1MB), $paths.Count) -ForegroundColor Green
foreach ($p in $paths) {
    $f = Get-Item -LiteralPath $p
    Write-Host ("    {0,-24} {1,8:N0} KB   {2:yyyy-MM-dd HH:mm}" -f
                $f.Name, ($f.Length / 1KB), $f.LastWriteTime) -ForegroundColor DarkGray
}
Write-Host "    Derived, never authoritative - rebuild it, do not edit it." -ForegroundColor DarkGray
