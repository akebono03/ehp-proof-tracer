param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r45r1_pytest_importmode_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R45R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R45R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r45r1_pytest_importmode_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R45R1 guarded patch failed' }
    powershell -NoProfile -ExecutionPolicy Bypass `
      -File '.\phase174_r3_r7_r45_ehp_open_obligation_audit\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R45 focused audit or regression tests failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
      'phase174_r3_r7_r45r1_pytest_importmode_fix/tests/test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R45R1 repair regression failed' }
    Write-Output 'PHASE174_R3R7R45R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R45R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
