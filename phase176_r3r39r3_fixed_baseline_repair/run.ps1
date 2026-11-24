param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $arguments = @()
    if ($DryRun) { $arguments += '--dry-run' }
    & python -B -m phase176_r3r39r3_fixed_baseline_repair.repair @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R3R39R3 fixed baseline repair failed' }
    if ($DryRun) { return }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib .\phase176_r3r39r3_fixed_baseline_repair\test_repair.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R39R3 focused tests failed' }
    & python -B -m phase176_r3r39_public_equality_transport.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 DFS audit failed' }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        .\phase176_r3r39_public_equality_transport\tests\test_source.py `
        .\phase176_r3r38_equality_transport_isolated\tests\test_source.py `
        .\phase176_r3r34_composite_suspension_isolated\tests\test_source.py `
        .\phase176_r3r36_composite_right_hopf_isolated\tests\test_source.py `
        .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 focused tests failed' }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'git diff check failed' }
    Write-Host 'PHASE176_R3R39R3_GATE=PASS_R3R39R3_FIXED_BASELINE_FOCUSED_TESTS'
    Write-Host 'PHASE176_R3R39R3_FULL_PYTEST=NOT_RUN'
    Write-Host '(END)'
} finally {
    Pop-Location
}
