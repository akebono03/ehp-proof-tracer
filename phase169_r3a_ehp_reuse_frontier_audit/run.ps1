# Read-only audit. This runner does not fetch, checkout, reset, or patch files.
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
if (-not (Test-Path '.git')) { throw "Git repository not found: $repo" }
$head = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'git rev-parse HEAD failed' }
Write-Host "GIT_HEAD=$head"
Write-Host 'R3A_AUDIT_ONLY: source files, existing tests, and documentation are unchanged.'
& python -B (Join-Path $package 'audit.py')
$auditExit = $LASTEXITCODE
Write-Host "R3A_AUDIT_EXIT_CODE=$auditExit"
if ($auditExit -ne 0) { throw "R3A audit failed. Read $package\output\audit_error.txt" }
& python -B -m pytest -q --tb=short `
    tests/test_phase165_r3_recursive_search.py `
    tests/test_phase165_r8_rule_provider.py `
    tests/test_phase165_r12_r5_structure_bridge.py `
    tests/test_phase161_r3_backward_goal_schema.py `
    phase168_r3_39a_reference_accuracy/tests/test_phase168_r3_39a_reference_accuracy.py
$pytestExit = $LASTEXITCODE
Write-Host "R3A_FOCUSED_PYTEST_EXIT_CODE=$pytestExit"
if ($pytestExit -ne 0) { throw 'R3A focused pytest failed' }
Write-Host 'PHASE169_R3A_AUDIT_COMPLETE: no source changes; full suite not run.'
