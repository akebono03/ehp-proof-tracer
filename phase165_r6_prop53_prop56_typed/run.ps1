$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$test = Join-Path $root 'phase165_r6_prop53_prop56_typed\test_explicit_typed_components.py'
if (!(Test-Path $test)) { throw 'Target test file missing' }
python -m pytest -q $test
if ($LASTEXITCODE -ne 0) { throw 'Phase163 explicit typed targeted tests failed' }
Write-Host 'Phase163 typed Proposition 5.3 and 5.6 targeted PASS; full pytest NOT run'
