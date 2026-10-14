$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$package;$project"
python -m pytest -q "$package/test_phase165_r52_r22_rule_compatibility.py"
if ($LASTEXITCODE -ne 0) { throw 'R22 targeted pytest failed' }
python "$package/phase165_r52_r22_rule_compatibility.py" --root "$project" --output "$package/audit_output"
if ($LASTEXITCODE -ne 0) { throw 'R22 audit failed' }
Write-Output "Review: $package\audit_output\review.md"
Write-Output "Details: $package\audit_output\compatibility.json"
Write-Output 'R22 read-only audit completed; full pytest NOT run.'
