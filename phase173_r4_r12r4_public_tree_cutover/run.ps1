param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Module = 'phase173_r4_r12r4_public_tree_cutover.install'
$Applied = $false
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 173 R4-R12R4 git fetch failed'
    }

    python -m $Module --root . --dry-run
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 173 R4-R12R4 Preflight failed'
    }

    if ($DryRun) {
        python -m pytest -q phase173_r4_r12r4_public_tree_cutover/tests/test_install.py
        if ($LASTEXITCODE -ne 0) {
            throw 'Phase 173 R4-R12R4 static fixture tests failed'
        }
        Write-Output 'PHASE173_R4_R12R4_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R12R4_PRODUCTION_EDIT=NONE'
        return
    }

    python -m $Module --root . --apply
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 173 R4-R12R4 apply failed'
    }
    $Applied = $true

    python -m pytest -q `
        phase173_r4_r12r4_public_tree_cutover/tests `
        phase173_r4_r12_common_narrative/tests/test_projection.py `
        phase173_r4_r12_common_narrative/tests/test_install.py `
        phase173_r4_r13_narrative_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 173 R4-R12R4 focused pytest failed'
    }
    Write-Output 'PHASE173_R4_R12R4_FOCUSED_PYTEST=PASS'
    Write-Output 'PHASE173_R4_R12R4_PUBLIC_MODEL_RENDERER=CUTOVER'
    Write-Output 'PHASE173_R4_R12R4_PHASE_COMPLETED=False'
    Write-Output 'PHASE173_R4_R12R4_CENTRAL_RENDERER_REVIEW_PENDING=True'
}
catch {
    if ($Applied) {
        Write-Output 'PHASE173_R4_R12R4_FOCUSED_PYTEST_FAILED_ROLLBACK_START'
        python -m $Module --root . --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'PHASE173_R4_R12R4_ROLLBACK_FAILED_MANUAL_REVIEW_REQUIRED'
        }
        else {
            Write-Output 'PHASE173_R4_R12R4_ROLLBACK=PASS'
        }
    }
    throw
}
finally {
    Pop-Location
}
