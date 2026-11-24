param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $parameters = @()
    if ($DryRun) { $parameters += '--dry-run' }
    & python -B -m phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.audit @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R43R1 source guard failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated\tests\test_finite_cyclic_subgroup_lift.py `
            .\phase175_r3_pi73_hopf_lift\tests\test_rule.py `
            .\phase176_r3r42_root_backward_frontier_audit\tests\test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R43R1 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R43R1 git diff check failed' }
        & python -B -m phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R43R1 post-test guard failed' }
        Write-Host 'PHASE176_R3R43R1_GATE=PASS_R3R43R1_ISOLATED_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R43R1_NEW_MATH_RULES=1'
        Write-Host 'PHASE176_R3R43R1_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally {
    Pop-Location
}
