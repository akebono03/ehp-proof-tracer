param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r43r2_reviewed_tracked_change_guard.repair --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R43R2 Source Guard failed: review tracked paths; no reset was made' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R43R2_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r43r2_reviewed_tracked_change_guard.repair
    if ($LASTEXITCODE -ne 0) { throw 'R43R2 repair failed' }
    Write-Output 'PHASE174_R3R7R43R2_TEST_GROUP=PATCH_CONTRACT'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r43r2_reviewed_tracked_change_guard/tests/test_guard.py
    if ($LASTEXITCODE -ne 0) { throw 'R43R2 patch-contract pytest failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r43r1_r3_sha_pin_fix\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R43R1 DryRun failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r43r1_r3_sha_pin_fix\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R43R1/R43 audit failed' }
    Write-Output 'PHASE174_R3R7R43R2_RUN=PASS'
    Write-Output 'PHASE174_R3R7R43R2_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
