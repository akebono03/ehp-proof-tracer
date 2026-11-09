param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r52r2_registry_assertion_id_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R52R2 source preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R52R2_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r52r2_registry_assertion_id_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R52R2 guarded repair failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r52_public_kernel_source_bound_probe\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R52 probe audit or focused regression failed' }
    Write-Output 'PHASE174_R3R7R52R2_TEST_GROUP=R52R2_PATCH'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider '.\phase174_r3_r7_r52r2_registry_assertion_id_fix\tests\test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R52R2 patch focused pytest failed' }
    Write-Output 'PHASE174_R3R7R52R2_RUN=PASS'
    Write-Output 'PHASE174_R3R7R52R2_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
