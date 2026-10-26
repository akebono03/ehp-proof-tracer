$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Host 'Phase 169 R3F3: focused pytest collection repair; EHP terminal n=3 proposals'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
Write-Host '[0/4] Verify exact package payloads and active focused test files before patching'
$packageTest = Join-Path $package 'tests\test_phase169_r3f_ehp_terminal_subgoals.py'
$packageAudit = Join-Path $package 'audit.py'
$packageApply = Join-Path $package 'apply.py'
$fullFunction1 = Join-Path $package 'full_functions\shared_expansion_provider.py'
$fullFunction2 = Join-Path $package 'full_functions\expand_registered_ehp_terminal_goal.py'
$existingAdapterTest = Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py'
$existingEhpTest = Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py'
$requiredPaths = @($packageTest, $packageAudit, $packageApply, $fullFunction1, $fullFunction2, $existingAdapterTest, $existingEhpTest)
foreach ($required in $requiredPaths) {
  if (-not (Test-Path -LiteralPath $required -PathType Leaf)) { throw "R3F3_MISSING_REQUIRED_FILE=$required" }
}
# The retired Phase 59 fixture was removed from the repository. Do not collect
# the Phase 161 R4 test that still imports tests.test_phase59_n3_ehp_chain.
# The Phase 169 R3E test also asserts that terminal proposals are ABSENT;
# R3F is intentionally changing precisely that expectation, so do not collect it.
Write-Host "R3F3_PREFLIGHT_OK: verified $($requiredPaths.Count) files"
Write-Host '[1/4] Guarded patch against committed R3E1 baseline, retaining existing provider'
python -B "$package\apply.py" install
if ($LASTEXITCODE -ne 0) { throw "R3F3_APPLY_EXIT_CODE=$LASTEXITCODE" }
Write-Host '[2/4] Focused pytest (R3F cases, existing adapter and EHP backward rules)'
python -B -m pytest -q -p no:cacheprovider `
  "$packageTest" `
  "$existingAdapterTest" `
  "$existingEhpTest"
$test_code = $LASTEXITCODE
Write-Host "R3F3_FOCUSED_PYTEST_EXIT_CODE=$test_code"
if ($test_code -ne 0) {
  Write-Warning 'Focused tests failed; performing guarded two-file restoration.'
  python -B "$package\apply.py" restore
  if ($LASTEXITCODE -ne 0) { throw 'R3F3_RESTORE_FAILED: manually inspect two modified files' }
  throw "R3F3_FOCUSED_PYTEST_EXIT_CODE=$test_code"
}
Write-Host '[3/4] Actual screened pi5^3 EHP terminal-frontier audit'
python -B -m phase169_r3f3_focused_collection_repair.audit
$audit_code = $LASTEXITCODE
Write-Host "R3F3_AUDIT_EXIT_CODE=$audit_code"
if ($audit_code -ne 0) {
  Write-Warning 'Runtime audit failed; performing guarded two-file restoration.'
  python -B "$package\apply.py" restore
  if ($LASTEXITCODE -ne 0) { throw 'R3F3_RESTORE_FAILED: manually inspect two modified files' }
  throw "R3F3_AUDIT_EXIT_CODE=$audit_code"
}
Write-Host '[4/4] Completion'
Write-Host 'R3F3_COMPLETE: two terminals have typed backward proposals; no GIVEN introduced; full suite NOT run.'
