$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Host 'Phase 169 R3H: adopt precise (5.3) Hopf source, preserve EHP inference trust boundary'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
if ($LASTEXITCODE -ne 0) { throw 'R3H_GIT_HEAD_UNAVAILABLE' }
$required = @(
    (Join-Path $package 'apply.py'),
    (Join-Path $package 'audit.py'),
    (Join-Path $package 'phase169_r3h_source_registry.py'),
    (Join-Path $package 'full_functions\build_shared_typed_bridge.py'),
    (Join-Path $package 'tests\test_phase169_r3h_toda53_hopf_source.py'),
    (Join-Path $repo 'phase165_r52_r9_shared_math.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'phase166_r3g_toda45_registry_connection\test_r3g.py'),
    (Join-Path $repo 'phase165_r52_r27_r5_typed_references\test_r5_typed_references.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py')
)
Write-Host '[0/4] Verify exact package payload and active focused test paths'
foreach ($path in $required) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "R3H_MISSING_REQUIRED=$path" }
}
Write-Host "R3H_PREFLIGHT_OK: $($required.Count) paths verified"
Write-Host '[1/4] Guarded full-function replacement and explicit new source module'
python -B "$package\apply.py" install
if ($LASTEXITCODE -ne 0) { throw "R3H_APPLY_EXIT_CODE=$LASTEXITCODE" }
Write-Host '[2/4] Focused pytest only (no full suite)'
python -B -m pytest -q -p no:cacheprovider `
    (Join-Path $package 'tests\test_phase169_r3h_toda53_hopf_source.py') `
    (Join-Path $repo 'phase166_r3g_toda45_registry_connection\test_r3g.py') `
    (Join-Path $repo 'phase165_r52_r27_r5_typed_references\test_r5_typed_references.py') `
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py') `
    (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py')
$test_code = $LASTEXITCODE
Write-Host "R3H_FOCUSED_PYTEST_EXIT_CODE=$test_code"
if ($test_code -ne 0) {
    Write-Warning 'Focused tests failed; restoring function and deleting new module.'
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3H_RESTORE_FAILED' }
    throw "R3H_FOCUSED_PYTEST_EXIT_CODE=$test_code"
}
Write-Host '[3/4] Audit actual citation-screened pi4_2 and pi5_3 frontier'
python -B -m phase169_r3h_toda53_hopf_source.audit
$audit_code = $LASTEXITCODE
Write-Host "R3H_AUDIT_EXIT_CODE=$audit_code"
if ($audit_code -ne 0) {
    Write-Warning 'Audit failed; restoring function and deleting new module.'
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3H_RESTORE_FAILED' }
    throw "R3H_AUDIT_EXIT_CODE=$audit_code"
}
Write-Host '[4/4] Completion'
Write-Host 'R3H_COMPLETE: (5.3) is a prior cited GIVEN; pi5_3 remains partial; full suite NOT run.'
