param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r43r1_r3_sha_pin_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R43R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R43R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r43r1_r3_sha_pin_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R43R1 installer failed' }
    Write-Output 'PHASE174_R3R7R43R1_TEST_GROUP=PATCH_CONTRACT'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r43r1_r3_sha_pin_fix/tests/test_fix.py
    if ($LASTEXITCODE -ne 0) { throw 'R43R1 focused pytest failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r43_public_ehp_map_property_wiring\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'Original R43 DryRun failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r43_public_ehp_map_property_wiring\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'Original R43 audit failed' }
    Write-Output 'PHASE174_R3R7R43R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R43R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
