$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONPATH = $Root
Write-Host 'Phase 168 R1: focused package tests only'
python -m pytest '.\phase168_r1_pi42_audit\tests\test_audit.py' -q --tb=short
if ($LASTEXITCODE -ne 0) { throw 'Focused audit tests failed' }
Write-Host 'Read-only pi_4^2 active-search audit'
python '.\phase168_r1_pi42_audit\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'Audit reported errors; inspect results/audit.json' }
Write-Host 'DONE: phase168_r1_pi42_audit\results\audit.md'
