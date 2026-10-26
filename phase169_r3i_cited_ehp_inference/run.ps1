$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Host 'Phase 169 R3I: derive n=3 EHP terminals from citation-screened source GIVENs'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
if ($LASTEXITCODE -ne 0) { throw 'R3I_GIT_UNAVAILABLE' }
$required = @(
    (Join-Path $package 'apply.py'),
    (Join-Path $package 'audit.py'),
    (Join-Path $package 'full_functions\shared_expansion_provider.py'),
    (Join-Path $package 'full_functions\expand_cited_ehp_terminal_goal.py'),
    (Join-Path $package 'reviewed_r3h\build_shared_typed_bridge.py'),
    (Join-Path $package 'reviewed_r3h\phase169_r3h_source_registry.py'),
    (Join-Path $package 'tests\test_phase169_r3i_cited_ehp_inference.py'),
    (Join-Path $repo 'phase165_r52_r9_shared_math.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'phase169_r3h_source_registry.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py'),
    (Join-Path $repo 'phase166_r3g_toda45_registry_connection\test_r3g.py'),
    (Join-Path $repo 'phase169_r3h_toda53_hopf_source\tests\test_phase169_r3h_toda53_hopf_source.py'),
    (Join-Path $repo 'phase169_r3f3_focused_collection_repair\tests\test_phase169_r3f_ehp_terminal_subgoals.py')
)
Write-Host '[0/4] Verify complete code payload and active test paths'
foreach ($path in $required) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "R3I_MISSING_REQUIRED=$path" }
}
Write-Host "R3I_PREFLIGHT_OK: $($required.Count) files verified"
Write-Host '[1/4] Guarded two-file patch; preserve R3H literature source and historical rules'
python -B "$package\apply.py" install
if ($LASTEXITCODE -ne 0) { throw "R3I_APPLY_EXIT_CODE=$LASTEXITCODE" }
Write-Host '[2/4] Focused pytest only (no full suite)'
python -B -m pytest -q -p no:cacheprovider `
    (Join-Path $package 'tests\test_phase169_r3i_cited_ehp_inference.py') `
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py') `
    (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py') `
    (Join-Path $repo 'phase166_r3g_toda45_registry_connection\test_r3g.py') `
    (Join-Path $repo 'phase169_r3h_toda53_hopf_source\tests\test_phase169_r3h_toda53_hopf_source.py') `
    (Join-Path $repo 'phase169_r3f3_focused_collection_repair\tests\test_phase169_r3f_ehp_terminal_subgoals.py')
$test_code = $LASTEXITCODE
Write-Host "R3I_FOCUSED_PYTEST_EXIT_CODE=$test_code"
if ($test_code -ne 0) {
    Write-Warning 'Focused pytest failed; restoring both production modules to R3H state.'
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3I_RESTORE_FAILED' }
    throw "R3I_FOCUSED_PYTEST_EXIT_CODE=$test_code"
}
Write-Host '[3/4] Audit real citation-screened pi4^2 / pi5^3 proof context'
python -B -m phase169_r3i_cited_ehp_inference.audit
$audit_code = $LASTEXITCODE
Write-Host "R3I_AUDIT_EXIT_CODE=$audit_code"
if ($audit_code -ne 0) {
    Write-Warning 'Proof audit failed; restoring both production modules to R3H state.'
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3I_RESTORE_FAILED' }
    throw "R3I_AUDIT_EXIT_CODE=$audit_code"
}
Write-Host '[4/4] Completion'
Write-Host 'R3I_COMPLETE: cited GIVEN premises used in legitimate INFERENCE; no full pytest run.'
