param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r55r1_source_guard_type_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55R1 Source Guard preflight failed' }

    Write-Output 'PHASE174_R3R7R55R1_TEST_GROUP=R55R1_TYPE_FIX'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r55r1_source_guard_type_fix/tests/test_fix.py
    if ($LASTEXITCODE -ne 0) { throw 'R55R1 focused test contract failed' }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R55R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }

    python -B -m phase174_r3_r7_r55r1_source_guard_type_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R55R1 Source Guard repair failed' }

    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r55_common_exactness_intro\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R55 repaired DryRun failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r55_common_exactness_intro\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R55 repaired full audit or focused pytest failed' }

    Write-Output 'PHASE174_R3R7R55R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R55R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
