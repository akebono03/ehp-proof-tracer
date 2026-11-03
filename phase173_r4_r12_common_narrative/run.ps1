param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $Args = @('-B','-m','phase173_r4_r12_common_narrative.install','--root',$Root,'--dry-run')
    & python @Args
    if ($LASTEXITCODE -ne 0) { throw 'R4-R12 source review failed' }
    Write-Output 'PHASE173_R4_R12_ISOLATED_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        'phase173_r4_r12_common_narrative/tests/test_install.py' `
        'phase173_r4_r12_common_narrative/tests/test_projection.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R12 isolated tests failed' }
    Write-Output 'PHASE173_R4_R12_ISOLATED_PYTEST=PASS'
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R12_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R12_RESULT=PASS_DRY_RUN'
        exit 0
    }
    & python -B -m phase173_r4_r12_common_narrative.install --root $Root
    if ($LASTEXITCODE -ne 0) { throw 'R4-R12 install failed' }
    Write-Output 'PHASE173_R4_R12_REGRESSION_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        'phase173_r4_r12_common_narrative/tests/test_web.py' `
        'phase173_r4_r1_narrative_source_fix/tests/test_live.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R12 Web regressions failed' }
    Write-Output 'PHASE173_R4_R12_REGRESSION_PYTEST=PASS'
    & python -B -m phase173_r4_r12_common_narrative.verify
    if ($LASTEXITCODE -ne 0) { throw 'R4-R12 Web verification failed' }
    Write-Output 'PHASE173_R4_R12_RESULT=PASS'
} finally {
    Pop-Location
}
