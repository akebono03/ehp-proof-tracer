param(
    [switch]$DryRun,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($DryRun) {
    python -m phase171_r20r7_public_injected_nonzero.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20R7 preflight failed' }
    exit 0
}
python -m phase171_r20r7_public_injected_nonzero.install
if ($LASTEXITCODE -ne 0) { throw 'R20R7 install failed' }
if (-not $SkipTests) {
    Write-Host 'PHASE171_R20R7_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r20r7_public_injected_nonzero/tests/test_public_injected_nonzero.py' `
        'phase171_r20r7_public_injected_nonzero/tests/test_install.py' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_injective_nonzero_from_a_real_finite_cyclic_generator' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_prior_untyped_eta_composition_is_matched_by_registered_identity'
    if ($LASTEXITCODE -ne 0) { throw 'R20R7 focused pytest failed' }
    Write-Host 'PHASE171_R20R7_FOCUSED_PYTEST=PASS'
}
python -m phase171_r20r7_public_injected_nonzero.audit
if ($LASTEXITCODE -ne 0) { throw 'R20R7 public proof-route audit failed' }
git status -sb
git diff --stat
