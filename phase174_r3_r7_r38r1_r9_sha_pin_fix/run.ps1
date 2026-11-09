param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r38r1_r9_sha_pin_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R38R1 SHA pin Source Guard DryRun failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R38R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r38r1_r9_sha_pin_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R38R1 SHA pin repair failed' }
    Write-Output 'PHASE174_R3R7R38R1_TEST_GROUP=R38R1_PIN_CONTRACT'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider 'phase174_r3_r7_r38r1_r9_sha_pin_fix/tests/test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R38R1 focused pytest failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r38_source_bound_zero_image_public_wiring\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'Repaired R38 run failed' }
    Write-Output 'PHASE174_R3R7R38R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R38R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
