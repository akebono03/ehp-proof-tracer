$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Join-Path $root 'phase165_r6_2_r4_r10_candidate_trace'
if (-not (Test-Path -LiteralPath (Join-Path $folder 'audit.py'))) { throw 'Run from repository root' }
$env:PYTHONPATH = "$root;$folder"
python -m pytest -q (Join-Path $folder 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R10 focused tests failed' }
python (Join-Path $folder 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R10 diagnostic execution failed' }
Write-Host 'R4-R10 read-only trace finished; full pytest NOT run.'
