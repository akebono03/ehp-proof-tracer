$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$package;$project"
python -m pytest -q "$package/test_phase165_r52_r21_rule_inventory.py"
if ($LASTEXITCODE -ne 0) { throw 'R21 targeted pytest failed' }
python "$package/phase165_r52_r21_rule_inventory.py" --root "$project" --output "$package/audit_output"
if ($LASTEXITCODE -ne 0) { throw 'R21 inventory failed' }
Write-Output 'R21 read-only inventory completed; full pytest NOT run.'
