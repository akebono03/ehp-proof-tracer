$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $project 'toda_group_proof_narrative_renderer.py'))) { throw 'Run from repository root' }
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$project;$package;$previous"
    python (Join-Path $package 'apply.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-17 patch failed' }
    python -m pytest -q (Join-Path $package 'tests/test_phase168_r3_17_homomorphism_term.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-17 targeted pytest failed' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-17 terminology guard and regression: PASS; full suite not run.'
