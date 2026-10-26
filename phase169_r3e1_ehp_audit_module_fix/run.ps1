$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Host 'Phase 169 R3E1: re-run typed EHP provider check with fixed audit import path'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
Write-Host '[1/4] Guarded full-function replacement in one production module'
python -B "$package\apply.py" install
if ($LASTEXITCODE -ne 0) { throw "R3E1_APPLY_EXIT_CODE=$LASTEXITCODE" }
Write-Host '[2/4] Focused pytest only (no full suite)'
python -B -m pytest -q -p no:cacheprovider `
    ".\phase169_r3e1_ehp_audit_module_fix\tests\test_phase169_r3e_ehp_provider_connection.py" `
    ".\tests\test_phase161_r3_backward_goal_schema.py" `
    ".\phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py" `
    ".\phase165_r12_r24_web_search_connection\tests\test_phase165_r12_r24_web_search_connection.py" `
    ".\phase165_r12_r21_eta_generator_chain\tests\test_phase165_r12_r21_eta_generator_chain.py"
$test_code = $LASTEXITCODE
Write-Host "R3E1_FOCUSED_PYTEST_EXIT_CODE=$test_code"
if ($test_code -ne 0) {
    Write-Warning 'Focused tests failed; performing guarded restoration.'
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3E1_RESTORE_FAILED: inspect source manually' }
    throw "R3E1_FOCUSED_PYTEST_EXIT_CODE=$test_code"
}
Write-Host '[3/4] Audit actual pi4^2 and pi5^3 screened proof frontier'
python -B -m phase169_r3e1_ehp_audit_module_fix.audit
$audit_code = $LASTEXITCODE
Write-Host "R3E1_AUDIT_EXIT_CODE=$audit_code"
if ($audit_code -ne 0) {
    Write-Warning 'Actual proof-frontier audit failed; performing guarded restoration.'
    python -B "$package\apply.py" restore
    if ($LASTEXITCODE -ne 0) { throw 'R3E1_RESTORE_FAILED: inspect source manually' }
    throw "R3E1_AUDIT_EXIT_CODE=$audit_code"
}
Write-Host '[4/4] Completion'
Write-Host 'R3E1_COMPLETE: typed EHP proposals connected, no GIVEN created; full suite NOT run.'
