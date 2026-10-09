$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONPATH = $Root
python -m pytest '.\phase162_r4_b_reference_specialization_audit\tests\test_phase162_r4_b_reference_specialization_audit.py' -q
if ($LASTEXITCODE -ne 0) { throw 'R4-B focused audit tests failed' }
python '.\phase162_r4_b_reference_specialization_audit\audit_phase162_r4_b_reference_specialization.py'
if ($LASTEXITCODE -ne 0) { throw 'R4-B audit failed' }
Write-Host 'R4-B reference/specialization audit complete; no production changes; full suite not run.'
