param(
    [switch]$DryRun,
    [switch]$RightOnly,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root

$Audit = Join-Path $PSScriptRoot 'audit.py'
if (-not (Test-Path -LiteralPath $Audit)) {
    throw 'R20R4 audit.py is missing'
}

if ($DryRun) {
    & python -m phase171_r20r4_first_success_public_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20R4 dry-run failed' }
    return
}

if (-not $SkipTests) {
    Write-Output 'PHASE171_R20R4_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider `
        'phase171_r2j_r4_r9_r7_public_cyclic_root/tests/test_audit.py::test_generic_source_anchored_root_is_a_premise_proposal_only' `
        'phase171_r2j_r4_r9_r8_public_cardinality/tests/test_audit.py::test_end_groups_yield_only_one_typed_backward_obligation'
    if ($LASTEXITCODE -ne 0) { throw 'R20R4 focused pytest failed' }
    Write-Output 'PHASE171_R20R4_FOCUSED_PYTEST=PASS'
}

if ($RightOnly) {
    & python -m phase171_r20r4_first_success_public_audit.audit --right-only
} else {
    & python -m phase171_r20r4_first_success_public_audit.audit
}
if ($LASTEXITCODE -ne 0) { throw 'R20R4 read-only audit failed' }
