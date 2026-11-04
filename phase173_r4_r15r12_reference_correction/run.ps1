param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R12 fetch failed' }
    python -m phase173_r4_r15r12_reference_correction.install --root "$RepoRoot" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R12 source guard failed' }
    python -m pytest -q -p no:cacheprovider phase173_r4_r15r12_reference_correction/tests/test_static.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R12 static tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R12_DRY_RUN_TESTS=PASS'
        Write-Output 'PHASE173_R4_R15R12R2_STATIC_PYTEST=PASS'
        Write-Output 'PHASE173_R4_R15R12_PRODUCTION_EDIT=NONE'
    } else {
        python -m phase173_r4_r15r12_reference_correction.install --root "$RepoRoot" --install
        if ($LASTEXITCODE -ne 0) { throw 'R15R12 installation failed' }
        try {
            python -m pytest -q -p no:cacheprovider `
                phase173_r4_r15r12_reference_correction/tests/test_integration.py `
                phase172_r5_prior_reference_display/tests/test_projection.py `
                phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py `
                phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py `
                phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py
            if ($LASTEXITCODE -ne 0) { throw 'R15R12 focused tests failed' }
            Write-Output 'PHASE173_R4_R15R12_FOCUSED_PYTEST=PASS'
            Write-Output 'PHASE173_R4_R15R12R2_FOCUSED_PYTEST=PASS'
            python -m phase173_r4_r15r12_reference_correction.audit `
                --output (Join-Path $PSScriptRoot 'reference_report.json')
            if ($LASTEXITCODE -ne 0) { throw 'R15R12 Web audit failed' }
            Write-Output 'PHASE173_R4_R15R12_PHASE_COMPLETED=False'
            Write-Output 'PHASE173_R4_R15R12R2_AUDIT=PASS'
        } catch {
            python -m phase173_r4_r15r12_reference_correction.install --root "$RepoRoot" --restore
            if ($LASTEXITCODE -ne 0) { throw 'R15R12 rollback requires manual inspection' }
            throw
        }
    }
} finally {
    Pop-Location
}
