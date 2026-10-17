$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$dir = Join-Path $root 'phase165_r6_2_r4_r11_provider_audit'
if (-not (Test-Path -LiteralPath (Join-Path $dir 'audit.py'))) { throw 'Run from repository root after extraction' }
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $dir 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 targeted tests failed' }
python (Join-Path $dir 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 audit failed; check audit_output' }
Write-Host 'R4-R11 read-only audit completed; full pytest NOT run.'
