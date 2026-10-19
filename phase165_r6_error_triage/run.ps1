$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$log = Join-Path $root 'phase165_r6_audit_results\collection.log'
$out = Join-Path $root 'phase165_r6_audit_results\collection_error_triage.json'
if (-not (Test-Path $log)) { throw "Missing collection log: $log" }
python -m pytest -q '.\phase165_r6_error_triage\tests\test_triage.py'
if ($LASTEXITCODE -ne 0) { throw 'Triage unit tests failed' }
python '.\phase165_r6_error_triage\triage.py' --log $log --output $out
if ($LASTEXITCODE -ne 0) { throw 'Triage generation failed' }
Write-Host 'READ-ONLY triage finished. No full pytest run. Phase closure remains PENDING.'
