$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Host 'Phase 169 R3F2: EHP terminal n=3 typed prerequisite proposals'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
Write-Host '[0/4] Verify all package files and the actual test path before patching'
$packageTest = Join-Path $package 'tests\test_phase169_r3f_ehp_terminal_subgoals.py'
$packageAudit = Join-Path $package 'audit.py'
$packageApply = Join-Path $package 'apply.py'
$fullFunction1 = Join-Path $package 'full_functions\shared_expansion_provider.py'
$fullFunction2 = Join-Path $package 'full_functions\expand_registered_ehp_terminal_goal.py'
foreach ($required in @($packageTest, $packageAudit, $packageApply, $fullFunction1, $fullFunction2)) {
  if (-not (Test-Path -LiteralPath $required -PathType Leaf)) { throw "R3F2_MISSING_PACKAGE_FILE=$required" }
}
$relatedTests = @(
  '.\phase169_r3e1_ehp_audit_module_fix\tests\test_phase169_r3e_ehp_provider_connection.py',
  '.\phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py',
  '.\phase161_r4_literature_premise_matching\tests\test_phase161_r4_literature_premise_matching.py',
  '.\tests\test_phase161_r3_backward_goal_schema.py'
)
foreach ($related in $relatedTests) {
  if (-not (Test-Path -LiteralPath $related -PathType Leaf)) { throw "R3F2_MISSING_EXISTING_TEST=$related" }
}
Write-Host "R3F2_PREFLIGHT_OK: $packageTest"
Write-Host '[1/4] Guarded patch against committed R3E1 baseline, keeping existing EHP provider'
python -B "$package\apply.py" install
if ($LASTEXITCODE -ne 0) { throw "R3F2_APPLY_EXIT_CODE=$LASTEXITCODE" }
Write-Host '[2/4] Focused pytest only (no full suite)'
python -B -m pytest -q -p no:cacheprovider `
  "$packageTest" `
  ".\phase169_r3e1_ehp_audit_module_fix\tests\test_phase169_r3e_ehp_provider_connection.py" `
  ".\phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py" `
  ".\phase161_r4_literature_premise_matching\tests\test_phase161_r4_literature_premise_matching.py" `
  ".\tests\test_phase161_r3_backward_goal_schema.py"
$test_code = $LASTEXITCODE
Write-Host "R3F2_FOCUSED_PYTEST_EXIT_CODE=$test_code"
if ($test_code -ne 0) {
  Write-Warning 'Focused tests failed; performing guarded two-file restoration.'
  python -B "$package\apply.py" restore
  if ($LASTEXITCODE -ne 0) { throw 'R3F2_RESTORE_FAILED: manually inspect two modified files' }
  throw "R3F2_FOCUSED_PYTEST_EXIT_CODE=$test_code"
}
Write-Host '[3/4] Actual citation-screened pi5^3 EHP terminal frontier audit'
python -B -m phase169_r3f2_test_path_fix.audit
$audit_code = $LASTEXITCODE
Write-Host "R3F2_AUDIT_EXIT_CODE=$audit_code"
if ($audit_code -ne 0) {
  Write-Warning 'Runtime audit failed; performing guarded two-file restoration.'
  python -B "$package\apply.py" restore
  if ($LASTEXITCODE -ne 0) { throw 'R3F2_RESTORE_FAILED: manually inspect two modified files' }
  throw "R3F2_AUDIT_EXIT_CODE=$audit_code"
}
Write-Host '[4/4] Completion'
Write-Host 'R3F2_COMPLETE: terminal proposals connected; INFERENCE premises remain mandatory; full suite NOT run.'
