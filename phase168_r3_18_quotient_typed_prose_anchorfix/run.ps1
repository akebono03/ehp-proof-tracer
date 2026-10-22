$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $project 'toda_group_proof_narrative_shared_components.py'))) { throw 'Run from repository root' }
$oldPYTHONPATH=$env:PYTHONPATH
try {
    $env:PYTHONPATH="$project;$package;$oldPYTHONPATH"
    python (Join-Path $package 'patch.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-18 patch failed' }
    python -m pytest -q (Join-Path $package 'tests/test_phase168_r3_18_quotient_typed_prose.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-18 targeted tests failed' }
}
finally { $env:PYTHONPATH=$oldPYTHONPATH }
Write-Host 'R3-18 typed quotient prose: limited validation completed; full suite not run.'
