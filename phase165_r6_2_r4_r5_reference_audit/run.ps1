$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Join-Path $root 'phase165_r6_2_r4_r5_reference_audit'
if (-not (Test-Path -LiteralPath (Join-Path $folder 'audit.py'))) { throw 'Please run from repository root.' }
$env:PYTHONPATH = "$folder;$root"
python -m pytest -q (Join-Path $folder 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Audit unit tests failed' }
python (Join-Path $folder 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Reference audit failed' }
Write-Host 'Read-only reference audit completed; full pytest NOT run.'
