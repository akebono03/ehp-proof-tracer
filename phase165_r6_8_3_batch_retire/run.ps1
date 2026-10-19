$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python -m pytest -q '.\phase165_r6_8_3_batch_retire\tests\test_retire.py'
if ($LASTEXITCODE -ne 0) { throw 'Retirement safety tests failed; no changes applied' }
python '.\phase165_r6_8_3_batch_retire\retire.py' --root $root --apply
if ($LASTEXITCODE -ne 0) { throw 'Retirement command failed' }
