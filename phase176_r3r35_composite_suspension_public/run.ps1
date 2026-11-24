param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $installArgs = @()
    if ($DryRun) { $installArgs += '--dry-run' }
    & python -B -m phase176_r3r35_composite_suspension_public.installer @installArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R35 installation or DryRun failed' }
    if (-not $DryRun) {
        & python -B -m phase176_r3r35_composite_suspension_public.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R35 public audit failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r35_composite_suspension_public/tests/test_installer.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R35 installer tests failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r35_composite_suspension_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R35 public tests failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r34_composite_suspension_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R34 isolated regressions failed' }
        & python -B -m pytest -q -p no:cacheprovider tests/test_hopf_rules.py -k 'hopf_composition_formula or hopf_invariant_reaches_hopf_composition_formula'
        if ($LASTEXITCODE -ne 0) { throw 'Existing Hopf regressions failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Git diff check failed' }
        Write-Host 'PHASE176_R3R35_GATE=PASS_R3R35_PUBLIC_CONNECTED_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R35_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
