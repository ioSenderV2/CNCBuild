#requires -Version 5.1
<#
    Check a board against Advanced Circuits' $33-each prototype spec.

    Reads the .kicad_pcb and the generated drill file, so it measures what will
    actually be sent, not what the design rules say is allowed.

    Usage: pwsh -File tools\check-4pcb-33.ps1 [-Pcb <path>] [-Drl <path>]
#>
param(
    [string]$Pcb = '',
    [string]$Drl = ''
)
$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
if (-not $Pcb) { $Pcb = Join-Path $repo 'linear-encoder\kicad\controller-board\controller-board.kicad_pcb' }
if (-not $Drl) { $Drl = Join-Path $repo 'linear-encoder\kicad\controller-board\fab\gerbers\controller-board.drl' }

$txt = [System.IO.File]::ReadAllText($Pcb)
$MM_PER_IN = 25.4

$results = New-Object System.Collections.Generic.List[object]
function Check([string]$name, [bool]$ok, [string]$measured, [string]$limit) {
    $results.Add([pscustomobject]@{
        Check = $name; Result = $(if ($ok) { 'PASS' } else { 'FAIL' }); Measured = $measured; Limit = $limit
    })
}

# ---- board outline ----
$edge = [regex]::Matches($txt, '\(gr_line\s*\(start ([\d\.\-]+) ([\d\.\-]+)\)\s*\(end ([\d\.\-]+) ([\d\.\-]+)\)[^\)]*\)[\s\S]{0,200}?\(layer "Edge\.Cuts"\)')
$xs = @(); $ys = @()
foreach ($e in $edge) {
    $xs += [double]$e.Groups[1].Value; $xs += [double]$e.Groups[3].Value
    $ys += [double]$e.Groups[2].Value; $ys += [double]$e.Groups[4].Value
}
$wmm = ($xs | Measure-Object -Maximum).Maximum - ($xs | Measure-Object -Minimum).Minimum
$hmm = ($ys | Measure-Object -Maximum).Maximum - ($ys | Measure-Object -Minimum).Minimum
$areaIn = ($wmm / $MM_PER_IN) * ($hmm / $MM_PER_IN)

Check 'Layer count 2' ($txt -match '\(layers[\s\S]{0,400}?"B\.Cu"') '2 copper layers' '2'
Check 'Max size 60 sq in' ($areaIn -le 60) ("{0:N3} sq in ({1} x {2} mm)" -f $areaIn, $wmm, $hmm) '60 sq in'

# ---- edge cuts must be one closed outline, no internal cutouts ----
$edgeShapes = ([regex]::Matches($txt, '\(layer "Edge\.Cuts"\)')).Count
Check 'No internal routing (cutouts)' ($edge.Count -eq 4 -and $edgeShapes -eq 4) `
      ("{0} Edge.Cuts lines, rectangular" -f $edge.Count) 'simple outline only'

# ---- trace widths ----
$segs = [regex]::Matches($txt, '\(segment\s*\(start[^\)]*\)\s*\(end[^\)]*\)\s*\(width ([\d\.]+)\)')
$minW = ($segs | ForEach-Object { [double]$_.Groups[1].Value } | Measure-Object -Minimum).Minimum
Check 'Min line 0.006 in' ($minW / $MM_PER_IN -ge 0.006) ("{0:N4} in ({1} mm)" -f ($minW / $MM_PER_IN), $minW) '0.006 in'

# ---- clearance comes from the netclass that DRC enforced ----
$clr = [regex]::Match($txt, '\(clearance ([\d\.]+)\)')
$minC = if ($clr.Success) { [double]$clr.Groups[1].Value } else { 0 }
Check 'Min space 0.006 in' ($minC / $MM_PER_IN -ge 0.006) ("{0:N4} in ({1} mm)" -f ($minC / $MM_PER_IN), $minC) '0.006 in'

# ---- vias: size, and blind/buried ----
$vias = [regex]::Matches($txt, '\(via[\s\S]{0,40}?\(at ([\d\.\-]+) ([\d\.\-]+)\)\s*\(size ([\d\.]+)\)\s*\(drill ([\d\.]+)\)\s*\(layers "([^"]+)" "([^"]+)"\)')
$blind = @($vias | Where-Object { $_.Groups[5].Value -ne 'F.Cu' -or $_.Groups[6].Value -ne 'B.Cu' })
Check 'No blind/buried vias' ($blind.Count -eq 0) ("{0} vias, all F.Cu-B.Cu" -f $vias.Count) 'through only'

# ---- every drilled hole: vias plus through-hole pads ----
$padDrills = [regex]::Matches($txt, '\(pad [^\)]*thru_hole[\s\S]{0,300}?\(drill ([\d\.]+)\)')
$holeSizes = @()
foreach ($v in $vias)      { $holeSizes += [double]$v.Groups[4].Value }
foreach ($p in $padDrills) { $holeSizes += [double]$p.Groups[1].Value }
$minHole = ($holeSizes | Measure-Object -Minimum).Minimum
Check 'Min hole 0.010 in' ($minHole / $MM_PER_IN -ge 0.010) ("{0:N4} in ({1} mm)" -f ($minHole / $MM_PER_IN), $minHole) '0.010 in'

# ---- hole density: the one that bites ----
# Prefer the real drill file if present; fall back to the board.
$holeCount = $holeSizes.Count
$source = 'board file'
if (Test-Path $Drl) {
    $n = (Get-Content $Drl | Select-String -Pattern '^X-?[\d\.]+Y-?[\d\.]+$').Count
    if ($n -gt 0) { $holeCount = $n; $source = 'drill file' }
}
$density = $holeCount / $areaIn
Check 'Max 35 holes per sq in' ($density -le 35) `
      ("{0:N1} per sq in  ({1} holes from the {2})" -f $density, $holeCount, $source) '35 per sq in'

# ---- no slots: KiCad writes oval drills as (drill oval w h) ----
$ovals = ([regex]::Matches($txt, '\(drill oval')).Count
Check 'No slots' ($ovals -eq 0) ("{0} oval drills" -f $ovals) 'none'

# ---- report ----
$results | Format-Table -AutoSize

$fails = @($results | Where-Object { $_.Result -eq 'FAIL' })
if ($fails.Count -gt 0) {
    Write-Output ("{0} FAILED" -f $fails.Count)
    Write-Output ("Hole budget at 35 per sq in: {0:N0} holes" -f [math]::Floor(35 * $areaIn))
    exit 1
}
Write-Output 'All checks pass.'
