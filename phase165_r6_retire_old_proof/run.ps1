$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q "$PSScriptRoot\tests\test_cleanup.py"
if ($LASTEXITCODE -ne 0) { throw 'Safety tests failed; no deletion performed' }
python "$PSScriptRoot\cleanup.py" --root "$root" --apply
if ($LASTEXITCODE -ne 0) { throw 'Cleanup failed: inspect audit result and rollback if needed' }
