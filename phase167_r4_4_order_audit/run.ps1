$ErrorActionPreference = 'Stop'
$env:PYTHONPATH = (Get-Location).Path
Write-Host '=== Phase 167 R4-4 display audit ==='
python '.\phase167_r4_4_order_audit\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'Display order audit failed or incomplete' }
Write-Host '=== Limited pytest ==='
python -m pytest '.\phase167_r4_4_order_audit\test_order_audit.py' -q
if ($LASTEXITCODE -ne 0) { throw 'Limited pytest failed' }
Write-Host 'Full pytest was not run. No production code was changed.'
