param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner --check-only
    if ($LASTEXITCODE -ne 0) { throw 'R3R49 canonical import guard failed' }
    & python -B -m phase176_r3r49_hopf_image_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R3R49 preflight failed' }
    if (-not $DryRun) {
        $groups = @(
            'phase176_r3r49_hopf_image_frontier/tests/test_frontier.py',
            'phase176_r3r36_composite_right_hopf_isolated/tests/test_source.py',
            'phase176_r3r38_equality_transport_isolated/tests/test_source.py',
            'phase176_r3r40r1_eta_notation_bridge/tests/test_notation.py'
        )
        foreach ($group in $groups) {
            Write-Host ('PHASE176_R3R49_TEST_GROUP=' + $group)
            & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner $group
            if ($LASTEXITCODE -ne 0) { throw ('R3R49 focused pytest failed: ' + $group) }
        }
        & python -B -m phase176_r3r49_hopf_image_frontier.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R49 frontier audit failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R49 diff check failed' }
        Write-Host 'PHASE176_R3R49_GATE=PASS_R3R49_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R49_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally { Pop-Location }
