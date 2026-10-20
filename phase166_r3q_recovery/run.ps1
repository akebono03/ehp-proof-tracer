$ErrorActionPreference = 'Stop'
python (Join-Path $PSScriptRoot 'recover.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-Q recovery guard failed; tests not run' }
python -m pytest -q 'phase166_r3d_pi32_regression\tests\test_phase166_r3d_pi32_regression.py'
if ($LASTEXITCODE -ne 0) { throw 'Pi3^2 regression failed after recovery' }
Write-Host 'Recovery targeted regression PASS; R3-Q is NOT complete; full pytest NOT run.'
