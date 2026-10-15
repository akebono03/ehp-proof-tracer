$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $project 'phase165_r57_r24_candidate_discovery.py'))) {
    throw 'R24 module missing in project root. Install R24 first.'
}
if (-not (Test-Path (Join-Path $project 'phase165_r57_r23_conclusion_unification.py'))) {
    throw 'R23 module missing in project root. Install R23-R1 first.'
}
Copy-Item (Join-Path $package 'phase165_r57_r25_premise_generation.py') (Join-Path $project 'phase165_r57_r25_premise_generation.py') -Force
Write-Host 'R25 generic premise generation installed (new module only).'
python -m pytest -q (Join-Path $package 'test_phase165_r57_r25_premise_generation.py')
if ($LASTEXITCODE -ne 0) { throw 'R25 targeted pytest FAILED' }
Write-Host 'R25 targeted pytest PASSED; full pytest NOT run.'
