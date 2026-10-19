$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$dir = $PSScriptRoot
python -m pytest -q "$dir\tests\test_triage.py"
if ($LASTEXITCODE -ne 0) { throw 'Focused regression failed' }
python "$dir\triage.py" --root "$root"
if ($LASTEXITCODE -ne 0) { throw 'Audit stopped without changing existing files' }
