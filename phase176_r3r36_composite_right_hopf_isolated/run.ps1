param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $auditArgs = @()
    if ($DryRun) { $auditArgs += '--dry-run' }
    & python -B -m phase176_r3r36_composite_right_hopf_isolated.audit @auditArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R36 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r36_composite_right_hopf_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R36 isolated pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase171_r2h_prop22_cited_hopf/tests/test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'Proposition 2.2 existing pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r30_generic_hopf_substitution_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R30 existing pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r34_composite_suspension_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R34 existing pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Git diff --check failed' }
        Write-Host 'PHASE176_R3R36_GATE=PASS_R3R36_ISOLATED_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R36_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
