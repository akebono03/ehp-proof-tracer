$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path '.\phase165_r27_r13\audit_report.json')) { throw 'Run R27-R13-R1 first: missing phase165_r27_r13/audit_report.json' }
python '.\phase165_r27_r14\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R14 audit failed' }
python -m pytest -q '.\phase165_r27_r14\test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R14 targeted pytest failed' }
Write-Host 'R27-R14 read-only production-consumer triage completed; full pytest NOT run.'
