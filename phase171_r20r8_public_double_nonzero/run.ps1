param(
    [switch]$DryRun,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($DryRun) {
    python -m phase171_r20r8_public_double_nonzero.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20R8 preflight failed' }
    exit 0
}
python -m phase171_r20r8_public_double_nonzero.install
if ($LASTEXITCODE -ne 0) { throw 'R20R8 install failed' }
if (-not $SkipTests) {
    Write-Host 'PHASE171_R20R8_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r20r8_public_double_nonzero/tests/test_source.py' `
        'phase171_r20r8_public_double_nonzero/tests/test_install.py' `
        'phase171_r20r7_public_injected_nonzero/tests/test_public_injected_nonzero.py' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_typed_equality_transfers_nonzero_to_exact_double' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_nonzero_double_must_have_inferred_equality_and_image'
    if ($LASTEXITCODE -ne 0) { throw 'R20R8 focused pytest failed' }
    Write-Host 'PHASE171_R20R8_FOCUSED_PYTEST=PASS'
}
python -m phase171_r20r8_public_double_nonzero.audit
if ($LASTEXITCODE -ne 0) { throw 'R20R8 public route audit failed' }
git status -sb
git diff --stat
