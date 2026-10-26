$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Root = Split-Path -Parent $Package
Set-Location $Root
$env:PYTHONPATH = $Root
$env:PYTHONDONTWRITEBYTECODE = '1'

Write-Host 'Phase 169 R3C1: eta composition alias repair'
Write-Host 'Git HEAD:'
& git rev-parse --short HEAD
Write-Host '[1/4] Guarded replacement after previous R3C auto-restoration'
& python -B "$Package\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host '[2/4] Focused pytest only'
& python -B -m pytest `
    "$Package\tests\test_phase169_r3c1_eta_alias_repair.py" `
    "$Package\tests\test_phase169_r3c_eta_composition_image.py" `
    '.\phase165_r12_r21_eta_generator_chain\tests\test_phase165_r12_r21_eta_generator_chain.py' `
    '.\phase169_r3b_finite_cyclic_suspension\tests\test_phase169_r3b_finite_cyclic_suspension.py' `
    '.\tests\test_phase165_r3_recursive_search.py' `
    '.\tests\test_phase165_r12_r5_structure_bridge.py' `
    -q --tb=short
$TestCode = $LASTEXITCODE
Write-Host "R3C1_FOCUSED_PYTEST_EXIT_CODE=$TestCode"
if ($TestCode -ne 0) {
    Write-Warning 'Focused tests failed; attempting guarded restoration.'
    & python -B "$Package\restore.py"
    exit $TestCode
}

Write-Host '[3/4] Inspect actual screened pi5^3 image proof, not synthetic GIVEN'
& python -B "$Package\audit.py"
$AuditCode = $LASTEXITCODE
Write-Host "R3C1_AUDIT_EXIT_CODE=$AuditCode"
if ($AuditCode -ne 0) {
    Write-Warning 'Actual composite-image proof is not verified; restoring production file.'
    & python -B "$Package\restore.py"
    exit $AuditCode
}
Write-Host '[4/4] Completion'
Write-Host 'R3C1_COMPLETE: composite image proved from screened eta-family ancestors; full suite NOT run.'
