param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
Push-Location $Root
try {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw 'Python is not available on PATH'
    }
    & python -B -m phase173_r4_r11_zero_public_connection.install --root $Root --dry-run
    if ($LASTEXITCODE -ne 0) {
        throw 'R4-R11 source guard/DryRun failed'
    }
    Write-Output 'PHASE173_R4_R11_ISOLATED_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        'phase173_r4_r11_zero_public_connection/tests/test_install.py' `
        'phase173_r4_r11_zero_public_connection/tests/test_route.py'
    if ($LASTEXITCODE -ne 0) {
        throw 'R4-R11 isolated proof / Web trust gate failed; production not modified'
    }
    Write-Output 'PHASE173_R4_R11_ISOLATED_PYTEST=PASS'
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R11_DRY_RUN=PASS'
    }
    else {
        & python -B -m phase173_r4_r11_zero_public_connection.install --root $Root
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R11 guarded installation failed'
        }
        & python -B -m phase173_r4_r11_zero_public_connection.verify --root $Root
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R11 public proof and Web verification failed'
        }
        Write-Output 'PHASE173_R4_R11_REGRESSION_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r10_general_toda56_core/tests/test_core.py' `
            'phase173_r4_r7_source_first_rule/tests/test_rule.py' `
            'phase173_r4_r8_public_connection/tests/test_route.py' `
            'phase173_r4_r1_narrative_source_fix/tests/test_live.py'
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R11 focused regression pytest failed'
        }
        Write-Output 'PHASE173_R4_R11_REGRESSION_PYTEST=PASS'
        Write-Output 'PHASE173_R4_R11_RESULT=PASS'
    }
}
finally {
    Pop-Location
}
