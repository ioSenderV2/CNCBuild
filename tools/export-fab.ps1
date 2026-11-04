#requires -Version 5.1
<#
    Build the fabrication and assembly package for the controller board.

    Writes linear-encoder/kicad/controller-board/fab/ from scratch: gerbers, drill,
    pick-and-place centroid and BOM. Everything is plotted against the board's
    lower-left corner, so gerbers, drill and centroid share one origin.

    Run it after any layout change; do not hand-edit anything under fab/.
#>
param(
    [string]$KicadCli = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
)
$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
$dir  = Join-Path $repo 'linear-encoder\kicad\controller-board'
$pcb  = Join-Path $dir 'controller-board.kicad_pcb'
$sch  = Join-Path $dir 'controller-board.kicad_sch'
$fab  = Join-Path $dir 'fab'
$gerb = Join-Path $fab 'gerbers'

if (-not (Test-Path $KicadCli)) { throw "kicad-cli not found: $KicadCli" }
if (-not (Test-Path $pcb))      { throw "board not found: $pcb" }

# README.md is hand-written and lives in fab/; keep it across a rebuild.
$readme = Join-Path $fab 'README.md'
$keep = if (Test-Path $readme) { [System.IO.File]::ReadAllBytes($readme) } else { $null }

if (Test-Path $fab) { Remove-Item -Recurse -Force $fab }
New-Item -ItemType Directory -Force $gerb | Out-Null
if ($keep) { [System.IO.File]::WriteAllBytes($readme, $keep) }

Write-Output '== gerbers =='
& $KicadCli pcb export gerbers `
    --output $gerb `
    --layers 'F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts' `
    --check-zones `
    --no-protel-ext `
    --use-drill-file-origin `
    $pcb

Write-Output '== drill =='
& $KicadCli pcb export drill `
    --output "$gerb\" `
    --format excellon `
    --drill-origin plot `
    --excellon-units mm `
    --generate-map `
    --map-format gerberx2 `
    $pcb

Write-Output '== centroid, bottom-side SMD only =='
& $KicadCli pcb export pos `
    --output (Join-Path $fab 'controller-board-bottom-pos.csv') `
    --side back `
    --format csv `
    --units mm `
    --smd-only `
    --use-drill-file-origin `
    $pcb

Write-Output '== BOM =='
& $KicadCli sch export bom `
    --output (Join-Path $fab 'controller-board-bom.csv') `
    --fields 'Reference,Value,Footprint,${QUANTITY}' `
    --labels 'Refs,Value,Footprint,Qty' `
    --group-by 'Value,Footprint' `
    --sort-field 'Reference' `
    $sch

Write-Output '== zip for upload =='
Compress-Archive -Path "$gerb\*" -DestinationPath (Join-Path $fab 'controller-board-gerbers.zip') -Force

Write-Output '== done =='
Get-ChildItem $fab -Recurse -File |
    Sort-Object FullName |
    ForEach-Object { '{0,-44} {1,8:N0}' -f $_.FullName.Substring($fab.Length + 1), $_.Length }
