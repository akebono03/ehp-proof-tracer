param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $guardArgs = @()
    if ($DryRun) { $guardArgs += '--dry-run' }
    & python -B -m phase176_r3r39r2_git_state_guard.guard @guardArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R39R2 git state guard failed' }
    if ($DryRun) { return }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'worktree diff check failed' }
    & git diff --cached --check
    if ($LASTEXITCODE -ne 0) { throw 'index diff check failed' }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib .\phase176_r3r39r2_git_state_guard\test_guard.py .\phase176_r3r39r1_eol_repair\test_eol.py
    if ($LASTEXITCODE -ne 0) { throw 'Git state and EOL tests failed' }
    & python -B -m phase176_r3r39_public_equality_transport.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 DFS audit failed' }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        .\phase176_r3r39_public_equality_transport\tests\test_source.py `
        .\phase176_r3r38_equality_transport_isolated\tests\test_source.py `
        .\phase176_r3r34_composite_suspension_isolated\tests\test_source.py `
        .\phase176_r3r36_composite_right_hopf_isolated\tests\test_source.py `
        .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 focused tests failed' }
    Write-Host 'PHASE176_R3R39R2_GATE=PASS_R3R39R2_EXACT_PATCH_FOCUSED_TESTS'
    Write-Host 'PHASE176_R3R39R2_FULL_PYTEST=NOT_RUN'
    Write-Host '(END)'
} finally {
    Pop-Location
}
