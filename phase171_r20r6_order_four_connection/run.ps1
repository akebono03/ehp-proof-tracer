param(
    [switch]$DryRun,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($DryRun) {
    python -m phase171_r20r6_order_four_connection.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20R6 preflight failed' }
    exit 0
}
python -m phase171_r20r6_order_four_connection.install
if ($LASTEXITCODE -ne 0) { throw 'R20R6 installation failed' }
if (-not $SkipTests) {
    Write-Host 'PHASE171_R20R6_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r20r6_order_four_connection/tests/test_public_order_four.py' `
        'phase171_r20r6_order_four_connection/tests/test_install.py' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_order_four_uses_cardinality_and_nonzero_double' `
        'phase171_r2j_r4_r9_r7_public_cyclic_root/tests/test_audit.py::test_generic_source_anchored_root_is_a_premise_proposal_only'
    if ($LASTEXITCODE -ne 0) { throw 'R20R6 focused pytest failed' }
    Write-Host 'PHASE171_R20R6_FOCUSED_PYTEST=PASS'
}
python -m phase171_r20r6_order_four_connection.audit
if ($LASTEXITCODE -ne 0) { throw 'R20R6 source-anchored audit failed' }
git status -sb
git diff --stat
