param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r32r1_reviewed_head_handoff_fix.install --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R32R1 reviewed source guard failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R32R1_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m phase174_r3_r7_r32r1_reviewed_head_handoff_fix.install
if ($LASTEXITCODE -ne 0) { throw 'R32R1 guarded installation failed' }
& python -B -m phase174_r3_r7_r32_lower_delta_kernel_audit.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R32 repaired DryRun failed' }

& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  '.\phase174_r3_r7_r32r1_reviewed_head_handoff_fix\tests\test_patch.py'
if ($LASTEXITCODE -ne 0) { throw 'R32R1 patch tests failed' }

& powershell -NoProfile -ExecutionPolicy Bypass -File `
  '.\phase174_r3_r7_r32_lower_delta_kernel_audit\run.ps1'
if ($LASTEXITCODE -ne 0) { throw 'R32 repaired focused suite failed' }

Write-Output 'PHASE174_R3R7R32R1_RUN=PASS'
Write-Output 'PHASE174_R3R7R32R1_FULL_PYTEST=False'
Write-Output '(END)'
