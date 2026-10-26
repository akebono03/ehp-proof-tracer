$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Host 'Phase 169 R3I2: genuine pi5^3 proof-tree closure audit and cross-phase test update'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
if ($LASTEXITCODE -ne 0) { throw 'R3I2_GIT_UNAVAILABLE' }
$required = @(
    (Join-Path $package 'apply.py'),
    (Join-Path $package 'patch_r3h_tests.py'),
    (Join-Path $package 'audit.py'),
    (Join-Path $package 'full_functions\shared_expansion_provider.py'),
    (Join-Path $package 'full_functions\expand_cited_ehp_terminal_goal.py'),
    (Join-Path $package 'reviewed_r3h\build_shared_typed_bridge.py'),
    (Join-Path $package 'reviewed_r3h\phase169_r3h_source_registry.py'),
    (Join-Path $package 'reviewed_r3h\test_phase169_r3h_toda53_hopf_source.py'),
    (Join-Path $package 'full_tests\test_phase169_r3h_toda53_hopf_source.py'),
    (Join-Path $package 'tests\test_phase169_r3i_cited_ehp_inference.py'),
    (Join-Path $package 'tests\test_phase169_r3i2_proof_closure_audit.py'),
    (Join-Path $package 'tests\test_phase169_r3i2_import_regression.py'),
    (Join-Path $repo 'phase165_r52_r9_shared_math.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'phase169_r3h_source_registry.py'),
    (Join-Path $repo 'phase169_r3h_toda53_hopf_source\tests\test_phase169_r3h_toda53_hopf_source.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py'),
    (Join-Path $repo 'phase166_r3g_toda45_registry_connection\test_r3g.py'),
    (Join-Path $repo 'phase169_r3f3_focused_collection_repair\tests\test_phase169_r3f_ehp_terminal_subgoals.py')
)
Write-Host '[0/5] Check payload, reviewed test import, and known test paths'
foreach ($path in $required) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "R3I2_MISSING_REQUIRED=$path" }
}
$replacementTest = Get-Content -LiteralPath (Join-Path $package 'full_tests\test_phase169_r3h_toda53_hopf_source.py') -Raw -Encoding UTF8
if ($replacementTest -notmatch 'from phase165_r52_partial_proof import ProofSearchStatus') {
    throw 'R3I2_REVIEWED_TEST_IMPORT_MISSING'
}
Write-Host "R3I2_PREFLIGHT_OK: $($required.Count) files"
Write-Host '[1/5] Apply the unchanged R3I production functions'
python -B "$package\apply.py" install
if ($LASTEXITCODE -ne 0) { throw "R3I2_APPLY_EXIT_CODE=$LASTEXITCODE" }
Write-Host '[2/5] Adjust two Phase R3H tests to check their timeless contracts'
python -B "$package\patch_r3h_tests.py" install
if ($LASTEXITCODE -ne 0) {
    $code = $LASTEXITCODE
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3I2_RESTORE_FAILED' }
    throw "R3I2_TEST_PATCH_EXIT_CODE=$code"
}
Write-Host '[3/5] Focused pytest only (no full suite)'
python -B -m pytest -q -p no:cacheprovider `
    (Join-Path $package 'tests\test_phase169_r3i_cited_ehp_inference.py') `
    (Join-Path $package 'tests\test_phase169_r3i2_proof_closure_audit.py') `
    (Join-Path $package 'tests\test_phase169_r3i2_import_regression.py') `
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py') `
    (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py') `
    (Join-Path $repo 'phase166_r3g_toda45_registry_connection\test_r3g.py') `
    (Join-Path $repo 'phase169_r3h_toda53_hopf_source\tests\test_phase169_r3h_toda53_hopf_source.py') `
    (Join-Path $repo 'phase169_r3f3_focused_collection_repair\tests\test_phase169_r3f_ehp_terminal_subgoals.py')
$test_code = $LASTEXITCODE
Write-Host "R3I2_FOCUSED_PYTEST_EXIT_CODE=$test_code"
if ($test_code -ne 0) {
    Write-Warning 'Tests failed; revert legacy tests and both production modules.'
    python -B "$package\patch_r3h_tests.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3I2_RESTORE_TESTS_FAILED' }
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3I2_RESTORE_PRODUCTION_FAILED' }
    throw "R3I2_FOCUSED_PYTEST_EXIT_CODE=$test_code"
}
Write-Host '[4/5] Validate entire pi5^3 proof tree and source chronological order'
python -B -m phase169_r3i2_import_repair.audit
$audit_code = $LASTEXITCODE
Write-Host "R3I2_AUDIT_EXIT_CODE=$audit_code"
if ($audit_code -ne 0) {
    Write-Warning 'Proof audit failed; revert legacy tests and both production modules.'
    python -B "$package\patch_r3h_tests.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3I2_RESTORE_TESTS_FAILED' }
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3I2_RESTORE_PRODUCTION_FAILED' }
    throw "R3I2_AUDIT_EXIT_CODE=$audit_code"
}
Write-Host '[5/5] Completion'
Write-Host 'R3I2_COMPLETE: pi5^3 root proof tree verified, no full pytest run.'
