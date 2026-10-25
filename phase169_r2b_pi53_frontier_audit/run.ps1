# Phase 169 R2B: read-only diagnostic; never patches production files.
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
if (-not (Test-Path '.git')) { throw "No Git repository at: $repo" }
$reviewed = '28bac5f61267b4381aaeb4fd5a623623bc5f18ce'
$head = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'git rev-parse HEAD failed' }
Write-Host "GIT_HEAD=$head"
Write-Host "REVIEWED_HEAD=$reviewed"
if ($head -ne $reviewed) {
    Write-Host 'NOTICE: HEAD differs from reviewed commit; this run is diagnostic only.'
}
Write-Host 'MODIFIED_PRODUCTION_PATHS:'
& git status --short -- phase165_r52_r9_shared_math.py phase165_r3_recursive_search.py phase165_r55_nk_only_goal.py phase168_r3_37c_reference_projection.py
Write-Host 'R2B_AUDIT_ONLY: application files and tests will not be modified.'
& python -B (Join-Path $package 'audit.py')
$auditCode = $LASTEXITCODE
Write-Host "R2B_AUDIT_EXIT_CODE=$auditCode"
if ($auditCode -ne 0) { throw "Audit failed; inspect $package\output\audit_error.txt" }
& python -B -m pytest -q --tb=short `
    tests/test_phase165_r3_recursive_search.py `
    tests/test_phase165_r8_rule_provider.py `
    tests/test_phase165_r12_r5_structure_bridge.py `
    tests/test_phase161_r3_backward_goal_schema.py
$testCode = $LASTEXITCODE
Write-Host "R2B_FOCUSED_PYTEST_EXIT_CODE=$testCode"
if ($testCode -ne 0) { throw 'Focused pytest failed' }
Write-Host 'PHASE169_R2B_AUDIT_COMPLETE: no production patch; full suite not run.'
