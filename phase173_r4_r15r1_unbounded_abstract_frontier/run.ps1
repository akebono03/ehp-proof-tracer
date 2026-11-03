param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub fetch failed' }

    $Options = @('--root', $Root)
    if ($DryRun) { $Options += '--dry-run' }
    python -m phase173_r4_r15r1_unbounded_abstract_frontier.install @Options
    if ($LASTEXITCODE -ne 0) { throw 'R4-R15R1 preflight/apply failed' }

    python -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_patch_source.py
    if ($LASTEXITCODE -ne 0) { throw 'R4-R15R1 patch safety tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R1_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R1_PRODUCTION_EDIT=NONE'
        exit 0
    }

    python -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
      phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) {
        python -m phase173_r4_r15r1_unbounded_abstract_frontier.install --root $Root --rollback
        throw 'R4-R15R1 focused mathematical tests failed; rollback requested'
    }

    python -m phase173_r4_r15r1_unbounded_abstract_frontier.frontier
    if ($LASTEXITCODE -ne 0) {
        python -m phase173_r4_r15r1_unbounded_abstract_frontier.install --root $Root --rollback
        throw 'R4-R15R1 frontier audit failed; rollback requested'
    }
    Write-Output 'PHASE173_R4_R15R1_FOCUSED_PYTEST=PASS'
    Write-Output 'PHASE173_R4_R15R1_PRODUCTION_CORE=ABSTRACT_PRIORS_K_UNBOUNDED'
    Write-Output 'PHASE173_R4_R15R1_NAMED_GENERATOR_CERTIFICATION=PENDING'
    Write-Output 'PHASE173_R4_R15R1_PHASE_COMPLETED=False'
}
finally {
    Pop-Location
}
