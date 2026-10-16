$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Join-Path $root 'phase165_r6_2_r4_r7_canonical_reconciliation'
if (-not (Test-Path -LiteralPath (Join-Path $folder 'audit.py'))) { throw 'Run from repository root' }
$env:PYTHONPATH = "$root;$folder"
python -m pytest -q (Join-Path $folder 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Audit unit tests failed' }
python (Join-Path $folder 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Canonical reconciliation failed' }
Write-Host 'Canonical reconciliation audited; production unchanged; full pytest NOT run.'
