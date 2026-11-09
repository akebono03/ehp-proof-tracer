param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r43r3_staged_index_recovery.recover --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R43R3 reviewed index preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R43R3_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r43r3_staged_index_recovery.recover
    if ($LASTEXITCODE -ne 0) { throw 'R43R3 exact index recovery failed' }
    Write-Output 'PHASE174_R3R7R43R3_TEST_GROUP=INDEX_CONTRACT'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r43r3_staged_index_recovery/tests/test_recovery.py
    if ($LASTEXITCODE -ne 0) { throw 'R43R3 limited pytest failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r43r2_reviewed_tracked_change_guard\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R43R2 DryRun failed after safe index recovery' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r43r2_reviewed_tracked_change_guard\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R43R2/R43R1/R43 validation failed' }
    Write-Output 'PHASE174_R3R7R43R3_RUN=PASS'
    Write-Output 'PHASE174_R3R7R43R3_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
