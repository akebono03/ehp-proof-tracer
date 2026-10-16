$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$dir = Join-Path $root 'phase165_r6_2_r4_r9_web_reconciliation'
if (-not (Test-Path -LiteralPath (Join-Path $dir 'audit.py'))) { throw 'Run from the repository root after extraction' }
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $dir 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R9 focused tests failed' }
python (Join-Path $dir 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R9 audit failed; inspect audit_output' }
Write-Host 'R4-R9 read-only reconciliation finished; full pytest NOT run.'
