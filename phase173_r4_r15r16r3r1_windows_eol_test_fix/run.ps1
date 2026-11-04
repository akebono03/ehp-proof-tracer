param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 Git fetch failed' }

    python -m phase173_r4_r15r16r3r1_windows_eol_test_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 source guard failed' }

    python -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r16r3r1_windows_eol_test_fix/test_staged_guard.py `
      phase173_r4_r15r16r3r1_windows_eol_test_fix/tests/test_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 corrected test preview failed' }

    if ($DryRun) {
        Write-Output 'R15R16R3R1_DRY_RUN=PASS'
        Write-Output 'R15R16R3R1_PRODUCTION_EDIT=NONE'
        Write-Output 'R15R16R3R1_FULL_PYTEST_RUN=False'
        exit 0
    }

    python -m phase173_r4_r15r16r3r1_windows_eol_test_fix.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 test correction failed' }
    try {
        powershell -NoProfile -ExecutionPolicy Bypass `
          -File '.\phase173_r4_r15r16r3_staged_guard_fix\run.ps1' -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 corrected original DryRun failed' }
        powershell -NoProfile -ExecutionPolicy Bypass `
          -File '.\phase173_r4_r15r16r3_staged_guard_fix\run.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 focused integration failed' }
        Write-Output 'R15R16R3R1_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R16R3R1_FULL_PYTEST_RUN=False'
        Write-Output 'R15R16R3R1_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r16r3r1_windows_eol_test_fix.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 test rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}
