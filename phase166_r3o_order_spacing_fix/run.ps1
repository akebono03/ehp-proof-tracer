$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
$pkg = Join-Path $root 'phase166_r3o_order_spacing_fix'
python (Join-Path $pkg 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Phase 166 R3-O corrected patch failed' }
python -m pytest -q (Join-Path $pkg 'test_phase166_r3o.py')
if ($LASTEXITCODE -ne 0) { throw 'Phase 166 R3-O focused tests failed; restore from backup' }
Write-Host 'Phase 166 R3-O focused tests PASS; full pytest NOT run.'
