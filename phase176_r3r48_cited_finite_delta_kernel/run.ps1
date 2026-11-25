param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $parameters = @()
    if ($DryRun) { $parameters += '--dry-run' }
    & python -B -m phase176_r3r48_cited_finite_delta_kernel.apply @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R48 guarded patch failed' }
    & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner --check-only
    if ($LASTEXITCODE -ne 0) { throw 'R3R48 canonical import check failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R48_GATE=PASS_R3R48_DRYRUN'
    } else {
        $groups = @(
            'phase176_r3r48_cited_finite_delta_kernel/tests/test_rule.py',
            'phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py',
            'phase176_r3r47_finite_cyclic_kernel_frontier/tests/test_frontier.py',
            'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py',
            'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/tests/test_finite_cyclic_subgroup_lift.py'
        )
        foreach ($group in $groups) {
            Write-Host ('PHASE176_R3R48_TEST_GROUP=' + $group)
            & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner $group
            if ($LASTEXITCODE -ne 0) { throw ('R3R48 focused pytest failed: ' + $group) }
        }
        Write-Host 'PHASE176_R3R48_GATE=PASS_R3R48_FOCUSED_TESTS'
        & python -B -m phase176_r3r48_cited_finite_delta_kernel.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R48 public kernel audit failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R48 git diff check failed' }
        Write-Host 'PHASE176_R3R48_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally { Pop-Location }
