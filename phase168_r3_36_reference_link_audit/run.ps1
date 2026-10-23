$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$bundle = $PSScriptRoot
$env:PYTHONPATH = "$bundle;$root"
python "$bundle\audit.py" --root "$root" --output "$bundle\output\audit.json"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$bundle\tests\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R3-36 read-only linkage inspection completed. Full suite NOT run.'
