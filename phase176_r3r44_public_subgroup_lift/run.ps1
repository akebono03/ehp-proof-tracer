param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $parameters = @()
    if ($DryRun) { $parameters += '--dry-run' }
    & python -B -m phase176_r3r44_public_subgroup_lift.apply @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R44 patch guard failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R44_GATE=PASS_R3R44_DRYRUN'
    } else {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r44_public_subgroup_lift\tests\test_public_subgroup_lift.py `
            .\phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated\tests\test_finite_cyclic_subgroup_lift.py `
            .\phase176_r3r41_public_quadruple_connection\tests\test_public_connection.py `
            .\phase176_r3r42_root_backward_frontier_audit\tests\test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R44 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R44 git diff check failed' }
        & python -B -m phase176_r3r44_public_subgroup_lift.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R44 real Web audit failed' }
        Write-Host 'PHASE176_R3R44_GATE=PASS_R3R44_PUBLIC_CONNECTION_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R44_NEW_MATH_RULES=0'
        Write-Host 'PHASE176_R3R44_NEW_GIVEN=0'
        Write-Host 'PHASE176_R3R44_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally {
    Pop-Location
}
