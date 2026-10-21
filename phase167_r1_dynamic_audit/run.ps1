$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
python ".\phase167_r1_dynamic_audit\audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
