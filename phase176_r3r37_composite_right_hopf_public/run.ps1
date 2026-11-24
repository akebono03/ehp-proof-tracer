param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $installArgs = @()
    if ($DryRun) { $installArgs += '--dry-run' }
    & python -B -m phase176_r3r37_composite_right_hopf_public.installer @installArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R37 installer or DryRun failed' }
    if (-not $DryRun) {
        & python -B -m phase176_r3r37_composite_right_hopf_public.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R37 public audit failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r37_composite_right_hopf_public/tests/test_installer.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R37 installer pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r37_composite_right_hopf_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R37 public pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r36_composite_right_hopf_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R36 isolated regression failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r35_composite_suspension_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R35 public regression failed' }
        & python -B -m pytest -q -p no:cacheprovider phase171_r2h_prop22_cited_hopf/tests/test_cited_formula.py -k 'right_formula_requires_screened_source or right_formula_rejects_wrong_rhs_and_bad_dimensions'
        if ($LASTEXITCODE -ne 0) { throw 'Legacy Proposition 2.2 regression failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Git diff check failed' }
        Write-Host 'PHASE176_R3R37_GATE=PASS_R3R37_PUBLIC_CONNECTED_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R37_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
