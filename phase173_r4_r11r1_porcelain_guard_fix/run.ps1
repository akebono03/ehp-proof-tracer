param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
Push-Location $Root
try {
    & python -B -m phase173_r4_r11r1_porcelain_guard_fix.repair --root $Root --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4-R11R1 source guard failed' }
    Write-Output 'PHASE173_R4_R11R1_FOCUSED_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        'phase173_r4_r11r1_porcelain_guard_fix/tests/test_repair.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R11R1 focused pytest failed' }
    Write-Output 'PHASE173_R4_R11R1_FOCUSED_PYTEST=PASS'
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R11R1_DRY_RUN=PASS'
    }
    else {
        & python -B -m phase173_r4_r11r1_porcelain_guard_fix.repair --root $Root
        if ($LASTEXITCODE -ne 0) { throw 'R4-R11R1 installation failed' }
        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase173_r4_r11_zero_public_connection\run.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'R4-R11 public verification/regression failed' }
        Write-Output 'PHASE173_R4_R11R1_RESULT=PASS'
    }
}
finally { Pop-Location }
