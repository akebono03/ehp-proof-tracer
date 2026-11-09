param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r40r1_matcher_order_test_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R40R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R40R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r40r1_matcher_order_test_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R40R1 focused test correction failed' }
    Write-Output 'PHASE174_R3R7R40R1_TEST_GROUP=R40R1_PATCH_CONTRACT'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r40r1_matcher_order_test_fix/tests/test_patch.py
    if ($LASTEXITCODE -ne 0) { throw 'R40R1 patch contract failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r40_adopted_db_zero_image_isolated\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R40 original focused audit failed after correction' }
    Write-Output 'PHASE174_R3R7R40R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R40R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
