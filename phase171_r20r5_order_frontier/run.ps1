param(
    [switch]$DryRun,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not $DryRun -and -not $SkipTests) {
    Write-Host 'PHASE171_R20R5_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_order_four_uses_cardinality_and_nonzero_double' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_nonzero_double_must_have_inferred_equality_and_image' `
        'phase171_r2j_r4_r9_r7_public_cyclic_root/tests/test_audit.py::test_generic_source_anchored_root_is_a_premise_proposal_only'
    if ($LASTEXITCODE -ne 0) { throw 'R20R5 focused pytest failed' }
    Write-Host 'PHASE171_R20R5_FOCUSED_PYTEST=PASS'
}
$arguments = @('-m', 'phase171_r20r5_order_frontier.audit')
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { throw 'R20R5 read-only audit failed' }
git status -sb
