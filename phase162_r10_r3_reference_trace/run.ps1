$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m phase162_r10_r3_reference_trace.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest -q .\phase162_r10_r3_reference_trace\tests\test_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R10-R3 read-only audit done. Full suite not run.'
