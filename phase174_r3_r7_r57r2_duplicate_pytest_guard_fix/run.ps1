param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r57r2_duplicate_pytest_guard_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R57R2 source guard or test-patch review failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R57R2_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r57r2_duplicate_pytest_guard_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R57R2 guarded test + installer correction failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r57r2_duplicate_pytest_guard_fix/tests/test_patch.py
    if ($LASTEXITCODE -ne 0) { throw 'R57R2 focused patch tests failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r57_narrative_source_cleanup\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'corrected R57 DryRun failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r57_narrative_source_cleanup\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'corrected R57 focused tests or public proof audit failed' }
    Write-Output 'PHASE174_R57R2_FULL_PYTEST=False'
    Write-Output 'PHASE174_R57R2_GATE=PASS_R57R2_FOCUSED_AND_R57_PUBLIC'
    Write-Output '(END)'
} finally {
    Pop-Location
}
