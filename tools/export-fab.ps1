#requires -Version 5.1
<#
    Build the fabrication and assembly package for the controller board.

    Writes linear-encoder/kicad/controller-board/fab/ from scratch: gerbers, drill,
    pick-and-place centroid and BOM. Everything is plotted against the board's
    lower-left corner, so gerbers, drill and centroid share one origin.

    Two vendor packages are built from the same plot pass, so they cannot drift:
      fab/pcbway/  - board + assembly: gerber zip, SMD-only BOM in PCBWay's
                     column layout, centroid with their headers, ASSEMBLY.md
      fab/oshpark/ - bare board: the gerber zip alone (OSH Park does no assembly;
                     they also accept the .kicad_pcb file directly)

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

# README.md and ASSEMBLY.md are hand-written and live in fab/; keep them across a rebuild.
$handWritten = @('README.md', 'ASSEMBLY.md')
$keep = @{}
foreach ($n in $handWritten) {
    $p = Join-Path $fab $n
    if (Test-Path $p) { $keep[$n] = [System.IO.File]::ReadAllBytes($p) }
}

if (Test-Path $fab) { Remove-Item -Recurse -Force $fab }
New-Item -ItemType Directory -Force $gerb | Out-Null
foreach ($n in $keep.Keys) { [System.IO.File]::WriteAllBytes((Join-Path $fab $n), $keep[$n]) }

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

Write-Output '== zip: bare board =='
Compress-Archive -Path "$gerb\*" -DestinationPath (Join-Path $fab 'controller-board-gerbers.zip') -Force

# The gerber zip alone cannot be quoted for assembly: it carries no BOM, no
# centroid and no statement of which parts to leave off. That is a second zip.
Write-Output '== zip: assembly =='
$asmParts = @(
    (Join-Path $fab 'ASSEMBLY.md')
    (Join-Path $fab 'controller-board-bom.csv')
    (Join-Path $fab 'controller-board-bottom-pos.csv')
) | Where-Object { Test-Path $_ }
Compress-Archive -Path $asmParts -DestinationPath (Join-Path $fab 'controller-board-assembly.zip') -Force

Write-Output '== vendor package: pcbway =='
$pcbway = Join-Path $fab 'pcbway'
New-Item -ItemType Directory -Force $pcbway | Out-Null
Copy-Item (Join-Path $fab 'controller-board-gerbers.zip') (Join-Path $pcbway 'controller-board-gerbers.zip')
if (Test-Path (Join-Path $fab 'ASSEMBLY.md')) {
    Copy-Item (Join-Path $fab 'ASSEMBLY.md') (Join-Path $pcbway 'ASSEMBLY.md')
}

# SMD-only BOM in PCBWay's preferred columns. The through-hole connectors are
# customer-fitted and deliberately absent here; ASSEMBLY.md says so in prose.
$bomAll = Import-Csv (Join-Path $fab 'controller-board-bom.csv')
$bomSmd = $bomAll | Where-Object { $_.Footprint -match '^(Capacitor|Resistor)_SMD:' } |
    ForEach-Object {
        [pscustomobject]@{
            'Designator'  = $_.Refs
            'Qty'         = $_.Qty
            'Value'       = $_.Value
            'Package'     = ($_.Footprint -split ':')[-1]
            'Type'        = 'SMD'
            'Description' = 'tolerance/voltage not critical - quote house-standard stock'
        }
    }
if (-not $bomSmd -or @($bomSmd).Count -lt 3) { throw 'SMD BOM filter produced fewer than 3 rows - check the BOM export' }
$bomSmd | Export-Csv -Path (Join-Path $pcbway 'controller-board-bom-smd.csv') -NoTypeInformation

# Centroid with PCBWay's headers, from the same kicad pos export.
$pos = Import-Csv (Join-Path $fab 'controller-board-bottom-pos.csv')
if (-not $pos -or @($pos).Count -lt 3) { throw 'centroid import produced fewer than 3 rows - check the pos export' }
$pos | ForEach-Object {
        [pscustomobject]@{
            'Designator' = $_.Ref
            'Mid X'      = $_.PosX
            'Mid Y'      = $_.PosY
            'Layer'      = if ($_.Side -eq 'bottom') { 'Bottom' } else { 'Top' }
            'Rotation'   = $_.Rot
        }
    } | Export-Csv -Path (Join-Path $pcbway 'controller-board-centroid.csv') -NoTypeInformation

Write-Output '== vendor package: oshpark =='
$oshpark = Join-Path $fab 'oshpark'
New-Item -ItemType Directory -Force $oshpark | Out-Null
Copy-Item (Join-Path $fab 'controller-board-gerbers.zip') (Join-Path $oshpark 'controller-board-gerbers.zip')

Write-Output '== done =='
Get-ChildItem $fab -Recurse -File |
    Sort-Object FullName |
    ForEach-Object { '{0,-44} {1,8:N0}' -f $_.FullName.Substring($fab.Length + 1), $_.Length }
