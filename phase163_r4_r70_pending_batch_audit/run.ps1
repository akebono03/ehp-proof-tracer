$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$r51 = Join-Path $root 'phase163_r4_r51_output\review.json'
$r69 = Join-Path $root 'phase163_r4_r69_output\order_duplicate_audit.json'
if (-not (Test-Path -LiteralPath $r51 -PathType Leaf)) { throw "Missing R51 input: $r51" }
if (-not (Test-Path -LiteralPath $r69 -PathType Leaf)) { throw "Missing R69 input: $r69" }
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r70_pending_batch_audit\tests\test_phase163_r4_r70_pending_batch_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R70 focused pytest failed' }
python '.\phase163_r4_r70_pending_batch_audit\phase163_r4_r70_pending_batch_audit.py' --r51 $r51 --r69 $r69 --output '.\phase163_r4_r70_output'
if ($LASTEXITCODE -ne 0) { throw 'R70 audit failed' }
Write-Output 'R4-R70 complete. No production changes. Full pytest not run.'
