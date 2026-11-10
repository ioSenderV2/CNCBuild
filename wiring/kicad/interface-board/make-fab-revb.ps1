# Rebuild the Rev B OSH Park package - FOR A QUOTE, NOT AN ORDER.
#
#   pwsh -File make-fab-revb.ps1
#
# Run it after ANY board change. Two things here are deliberate and easy to undo
# by accident if this is ever done by hand again:
#
#   1. DRC runs first with --refill-zones --save-board, so the plot cannot ship a
#      stale fill. On this board that matters more than usual - the inner planes
#      and the two 36 V pours are most of the copper on it.
#   2. The drill MAP is written alongside but kept OUT of the zip. It is a .gbr
#      and OSH Park's uploader can mistake it for a copper layer.
#
# fab/oshpark/ is Rev A's order record and is never touched by this.

$ErrorActionPreference = 'Stop'
$cli = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$pcb = Join-Path $here 'interface-board.kicad_pcb'
$out = Join-Path $here 'fab\oshpark-revb'
$zip = Join-Path $out 'interface-board-revb-oshpark.zip'

$layers = 'F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts'

& $cli pcb drc --schematic-parity --severity-error --exit-code-violations --refill-zones --save-board $pcb
if ($LASTEXITCODE -ne 0) { throw "DRC is not clean - no package built" }

New-Item -ItemType Directory -Force $out | Out-Null
# Protel extensions are kicad-cli's default - --no-protel-ext would turn them OFF.
# --check-zones refills at plot time as well, belt and braces over the DRC above.
# ABSOLUTE origin on both, which is what the quote package already shipped: the
# outline plots at x 5..138, y 5..137. Gerbers and drill must share a frame, so
# these two lines change together or not at all.
& $cli pcb export gerbers --output $out --layers $layers --check-zones $pcb
& $cli pcb export drill --output $out --format excellon --drill-origin absolute --excellon-units mm --generate-map --map-format gerberx2 $pcb

$keep = @('interface-board-F_Cu.gtl', 'interface-board-In1_Cu.g1', 'interface-board-In2_Cu.g2',
          'interface-board-B_Cu.gbl', 'interface-board-F_Mask.gts', 'interface-board-B_Mask.gbs',
          'interface-board-F_Silkscreen.gto', 'interface-board-B_Silkscreen.gbo',
          'interface-board-F_Paste.gtp', 'interface-board-B_Paste.gbp',
          'interface-board-Edge_Cuts.gm1', 'interface-board-job.gbrjob', 'interface-board.drl')

$missing = $keep | Where-Object { -not (Test-Path (Join-Path $out $_)) }
if ($missing) { throw "export did not produce: $($missing -join ', ')" }

if (Test-Path $zip) { Remove-Item $zip }
Compress-Archive -Path ($keep | ForEach-Object { Join-Path $out $_ }) -DestinationPath $zip
Write-Output "zipped $($keep.Count) files into $zip"
