<#
.SYNOPSIS
  Regenerate everything derived, in dependency order, ending with the send-out zip.

.DESCRIPTION
  ONE ENTRY POINT, because the order matters and the chain was being run by hand.
  Every step reads the registry or something an earlier step wrote:

    1. dims.py check          the registry resolves. Nothing else runs if it does not
    2. dims.py md/html/fusion VALUES.md, registry.html, fusion-parameters.csv
    3. make-fasteners.py      fasteners.html          <- zip member
    4. make-box-doc.py        torsion-box-construction.html  <- zip member
       make-base-doc.py       base-construction.html         <- zip member
    5. make-3d.py             Interactive_Model.html  <- zip member
    6. build-hole-tally.py    the tallies inside shop-pack.html
    7. status.py all          STATUS.md and INDEX.md
    8. the six checkers       prism edges, clash, registry JS, shop pack refs,
                              subst - every {{SYMBOL}} resolves - and restale,
                              which fails if a registry value moved and prose
                              still quotes the old one
    9. make-pdf.ps1           the two documents and shop-pack.pdf, and make-pdf
                              then rebuilds "CNC Build.zip" itself - the zip
                              carries the pack, so it is bundled whenever the
                              pack prints

  WHY THE ZIP IS AT THE END AND NOT A STEP OF ITS OWN: three of its four members
  are written by steps 3 to 5 and the fourth is the pack from step 9. Zipping
  earlier would ship whatever was lying in machine/drawings from last time,
  which is exactly the stale-copy failure this repo generates STATUS.md to avoid.

  THE CHECKS RUN BEFORE THE PDFs ON PURPOSE. A failed check means the model or
  the pack is wrong, and printing it takes minutes - so the cheap verdict comes
  first. A check failure stops the run; pass -Force to print anyway.

.PARAMETER NoPdf
  Stop after the checks. Fast, and it leaves the PDFs and the zip STALE - the
  run says so rather than letting a half-regenerated bundle look finished.

.PARAMETER Audit
  Also run audit-prose.py, which reports near misses between the prose and the
  registry. Not in the default run: every hit needs judgement and most are fine.

.PARAMETER Force
  Carry on to the PDFs even if a checker failed.

.EXAMPLE
  pwsh -File tools\regen.ps1
  pwsh -File tools\regen.ps1 -NoPdf
#>
[CmdletBinding()]
param(
    [switch] $NoPdf,
    [switch] $Audit,
    [switch] $Force
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$py = 'python'

function Step {
    # NOT $Args: that is a PowerShell automatic variable, and a parameter of
    # that name arrives EMPTY - which launched python with no arguments, i.e.
    # the interactive REPL, and the run hung until it was killed.
    param([string] $Label, [string[]] $Argv)
    Write-Host "-- $Label" -ForegroundColor Cyan
    & $py @Argv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $Label" -ForegroundColor Red
        exit 1
    }
}

Push-Location $repo
try {
    # 1. the registry first. Everything below reads it, so a registry that does
    #    not resolve would otherwise be discovered four generators later.
    Step 'registry resolves' @('tools/dims.py', 'check')
    # the quote DXFs read the same hole schedules, so they go stale the same way
    Step 'quote DXFs' @('tools/make-dxf.py')

    # 2-7. the generators, in the order their outputs feed each other
    Step 'VALUES.md' @('tools/dims.py', 'md', '-o', 'dimensions/VALUES.md')
    Step 'registry.html' @('tools/dims.py', 'html', '-o', 'dimensions/registry.html')
    Step 'fusion-parameters.csv' `
        @('tools/dims.py', 'fusion', '-o', 'dimensions/fusion-parameters.csv')
    Step 'fasteners.html' @('tools/make-fasteners.py')
    Step 'torsion-box-construction.html' @('tools/make-box-doc.py')
    Step 'base-construction.html' @('tools/make-base-doc.py')
    Step 'base-cutlist.html' @('tools/make-cutlist-doc.py')
    Step 'Interactive_Model.html' @('tools/make-3d.py')
    Step 'shop pack hole tallies' @('tools/build-hole-tally.py')
    Step 'STATUS.md and INDEX.md' @('tools/status.py', 'all')

    # 8. the checkers. Cheap, and they are the reason to stop before printing.
    $bad = 0
    # subst is a GATE and audit-prose is not, which is the difference worth
    # knowing: a symbol either exists or it does not, so there is no judgement
    # to apply and no reason to let a document print with {{TYPO}} in it.
    # restale is the one that catches the failure this repo keeps hitting: a
    # registry value moves and the prose quoting it does not. It compares the
    # working tree against the registry AT HEAD, so it has to run BEFORE the
    # change is committed - which is where this sits.
    # check-note-history is a RATCHET, not an audit: it reads only the notes
    # this working tree changed, so it never argues with the existing corpus.
    # Like restale it compares against HEAD, so it also has to run uncommitted.
    # check-bearing is the INVERSE of check-clash-js: that one finds solids
    # that overlap and must not, this one finds surfaces that must meet and do
    # not. It is here because the front centre leg's shoulder was carrying
    # nothing in the drawn geometry and no check was asking.
    foreach ($c in 'check-prism-edges', 'check-clash-js', 'check-bearing',
                   'check-registry-js', 'check-shop-pack-refs',
                   'check-cutlist-nest', 'subst',
                   'restale', 'check-note-history') {
        Write-Host "-- $c" -ForegroundColor Cyan
        & $py "tools/$c.py" @(
            if ($c -eq 'subst') { '--check' }
            elseif ($c -eq 'restale') { '--since-git'; '--gate' })
        if ($LASTEXITCODE -ne 0) { $bad++; Write-Host "  FAILED" -ForegroundColor Red }
    }
    if ($Audit) {
        Write-Host '-- audit-prose (judgement, not a gate)' -ForegroundColor Cyan
        & $py 'tools/audit-prose.py'
    }
    if ($bad -and -not $Force) {
        Write-Host ''
        Write-Host "$bad checker(s) failed - stopping before the PDFs." -ForegroundColor Red
        Write-Host '  The PDFs and "CNC Build.zip" are now STALE. Fix, or re-run with -Force.' `
            -ForegroundColor DarkGray
        exit 1
    }

    if ($NoPdf) {
        Write-Host ''
        Write-Host 'Done, PDFs skipped.' -ForegroundColor Yellow
        Write-Host '  build-document.pdf, design-record.pdf, shop-pack.pdf and' `
            -ForegroundColor DarkGray
        Write-Host '  "CNC Build.zip" are STALE against what just regenerated.' `
            -ForegroundColor DarkGray
        exit 0
    }

    # 9. the documents and the pack - and make-pdf bundles the zip on a clean print
    Write-Host '-- documents, shop pack and the send-out zip' -ForegroundColor Cyan
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'make-pdf.ps1')
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'FAILED: make-pdf - the zip was not rebuilt' -ForegroundColor Red
        exit 1
    }

    Write-Host ''
    Write-Host 'Everything derived is current, zip included.' -ForegroundColor Green
}
finally {
    Pop-Location
}
