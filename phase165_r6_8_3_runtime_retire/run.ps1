$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
python -m pytest -q ".\phase165_r6_8_3_runtime_retire\tests\test_runtime_retire.py"
if ($LASTEXITCODE -ne 0) { throw 'Retirement safety tests failed; no files deleted' }
python ".\phase165_r6_8_3_runtime_retire\retire.py" --root "." --apply
if ($LASTEXITCODE -ne 0) { throw 'Runtime reachability was inconclusive; no files deleted' }
Write-Host 'Full pytest NOT run. Existing legacy tests may need R6-8(4) collection retirement.'
