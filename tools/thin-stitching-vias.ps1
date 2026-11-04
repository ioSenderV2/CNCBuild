#requires -Version 5.1
<#
    Thin the GND stitching vias on the controller board from the 4 mm placement
    grid down to an 8 mm subgrid.

    Advanced Circuits' $33 prototype spec caps drilled holes at 35 per square
    inch. The 4 mm stitching grid put the board at 40.1. Stitching is the only
    hole population on this board that is discretionary, so it is what gives.

    Only vias sitting exactly on the stitching grid are touched; routing vias
    and the header's holes are matched by position and left alone.

    -WhatIf reports what would go without writing.
#>
param(
    [string]$Pcb = '',
    [switch]$WhatIf
)
$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
if (-not $Pcb) { $Pcb = Join-Path $repo 'linear-encoder\kicad\controller-board\controller-board.kicad_pcb' }

# The grid add_gnd_stitching_vias used: 4 mm pitch from this corner.
$X0 = 100.95; $Y0 = 104.95; $PITCH = 4.0; $KEEP_EVERY = 2   # keep every 2nd -> 8 mm
$EPS = 0.001

function OnGrid([double]$v, [double]$origin, [double]$pitch) {
    $n = ($v - $origin) / $pitch
    return ([math]::Abs($n - [math]::Round($n)) -lt $EPS)
}
function GridIndex([double]$v, [double]$origin, [double]$pitch) {
    return [int][math]::Round(($v - $origin) / $pitch)
}

$bytes  = [System.IO.File]::ReadAllBytes($Pcb)
$hasBom = ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)
$txt    = [System.IO.File]::ReadAllText($Pcb)

# Whole via blocks, captured so they can be removed verbatim.
$rx = [regex]'(?m)^\t\(via\r?\n\t\t\(at ([\d\.\-]+) ([\d\.\-]+)\)\r?\n\t\t\(size [\d\.]+\)\r?\n\t\t\(drill [\d\.]+\)\r?\n\t\t\(layers "[^"]+" "[^"]+"\)\r?\n\t\t\(net "?([^")\r\n]+)"?\)\r?\n\t\t\(uuid "[^"]+"\)\r?\n\t\)\r?\n'

$all = $rx.Matches($txt)
Write-Output ("vias found: {0}" -f $all.Count)

$drop = New-Object System.Collections.Generic.List[object]
$keptStitch = 0; $routing = 0

foreach ($m in $all) {
    $x = [double]$m.Groups[1].Value
    $y = [double]$m.Groups[2].Value
    $net = $m.Groups[3].Value.Trim('"')

    $isStitch = ($net -eq 'GND') -and (OnGrid $x $X0 $PITCH) -and (OnGrid $y $Y0 $PITCH)
    if (-not $isStitch) { $routing++; continue }

    $ix = GridIndex $x $X0 $PITCH
    $iy = GridIndex $y $Y0 $PITCH
    if (($ix % $KEEP_EVERY -eq 0) -and ($iy % $KEEP_EVERY -eq 0)) { $keptStitch++ }
    else { $drop.Add($m) }
}

Write-Output ("routing / header vias untouched : {0}" -f $routing)
Write-Output ("stitching kept (8 mm subgrid)   : {0}" -f $keptStitch)
Write-Output ("stitching removed               : {0}" -f $drop.Count)

if ($WhatIf) { Write-Output 'WhatIf - nothing written.'; return }
if ($drop.Count -eq 0) { Write-Output 'Nothing to remove.'; return }

# Remove from the end so earlier offsets stay valid.
$sb = New-Object System.Text.StringBuilder $txt
foreach ($m in ($drop | Sort-Object { $_.Index } -Descending)) {
    [void]$sb.Remove($m.Index, $m.Length)
}

$enc = New-Object System.Text.UTF8Encoding($hasBom)
[System.IO.File]::WriteAllText($Pcb, $sb.ToString(), $enc)

$after = $rx.Matches([System.IO.File]::ReadAllText($Pcb)).Count
Write-Output ("vias now: {0}  (BOM preserved: {1})" -f $after, $hasBom)
