param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner --check-only
    if ($LASTEXITCODE -ne 0) { throw 'R3R50 canonical import guard failed' }
    if ($DryRun) {
        & python -B -m phase176_r3r50_strict_nu_prime_connection.apply --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R50 preflight failed' }
        Write-Host 'PHASE176_R3R50_GATE=PASS_R3R50_DRYRUN'
    } else {
        & python -B -m phase176_r3r50_strict_nu_prime_connection.apply
        if ($LASTEXITCODE -ne 0) { throw 'R3R50 apply failed' }
        $groups = @(
            'phase176_r3r50_strict_nu_prime_connection/tests/test_notation_connection.py',
            'phase176_r3r49_hopf_image_frontier/tests/test_frontier.py',
            'phase176_r3r41_public_quadruple_connection/tests/test_public_connection.py',
            'phase176_r3r40r1_eta_notation_bridge/tests/test_notation.py',
            'phase175_r4r12r13r7_typed_nu_prime_notation/tests/test_r13r7_notation.py',
            'phase176_r3r48_cited_finite_delta_kernel/tests/test_rule.py'
        )
        foreach ($group in $groups) {
            Write-Host ('PHASE176_R3R50_TEST_GROUP=' + $group)
            & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner $group
            if ($LASTEXITCODE -ne 0) { throw ('R3R50 focused pytest failed: ' + $group) }
        }
        Write-Host 'PHASE176_R3R50_GATE=PASS_R3R50_FOCUSED_TESTS'
        & python -B -m phase176_r3r50_strict_nu_prime_connection.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R50 public audit failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R50 diff check failed' }
        Write-Host 'PHASE176_R3R50_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally { Pop-Location }
