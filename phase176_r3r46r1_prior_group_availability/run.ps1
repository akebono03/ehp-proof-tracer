param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $parameters = @()
    if ($DryRun) { $parameters += '--dry-run' }
    & python -B -m phase176_r3r46r1_prior_group_availability.apply @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 guarded patch failed' }
    & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner --check-only
    if ($LASTEXITCODE -ne 0) { throw 'R3R46R2 canonical import check failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R46R1_GATE=PASS_R3R46R1_DRYRUN'
        Write-Host 'PHASE176_R3R46R2_GATE=PASS_R3R46R2_IMPORT_DRYRUN'
    } else {
        $groups = @(
            'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py',
            'phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py',
            'phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py',
            'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
            'phase176_r3r45_direct_premise_audit/tests/test_audit.py',
            'tests/test_phase165_r3_recursive_search.py'
        )
        foreach ($group in $groups) {
            Write-Host ('PHASE176_R3R46R2_TEST_GROUP=' + $group)
            & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner $group
            if ($LASTEXITCODE -ne 0) { throw ('R3R46R2 focused pytest failed: ' + $group) }
        }
        Write-Host 'PHASE176_R3R46R2_GATE=PASS_R3R46R2_ISOLATED_FOCUSED_TESTS'
        & python -B -m phase176_r3r46r1_prior_group_availability.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 Web audit failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 diff check failed' }
        Write-Host 'PHASE176_R3R46R1_GATE=PASS_R3R46R1_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R46R2_GATE=PASS_R3R46R2_RESUMED_PUBLIC_AUDIT'
        Write-Host 'PHASE176_R3R46R1_NEW_MATH_RULES=0'
        Write-Host 'PHASE176_R3R46R1_NEW_GIVEN_REGISTRATIONS=0'
        Write-Host 'PHASE176_R3R46R1_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally { Pop-Location }
