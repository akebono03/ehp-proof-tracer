$ErrorActionPreference = 'Stop'
if (-not (Test-Path 'web_app.py')) { throw 'Run from the repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R52-R4 installation failed' }
$tests = @(
  'test_phase165_r52_r4_flask_connection.py',
  'test_phase165_r52_r3_web_adapter.py',
  'test_phase165_r52_r3_empty_steps_contract.py',
  'test_phase165_r52_r2_search_adapter.py',
  'test_phase165_r52_r2_engine_observer.py',
  'test_phase165_r52_partial_proof.py',
  'tests/test_phase165_r3_recursive_search.py',
  'tests/test_phase165_r9_production_wiring.py',
  'tests/test_phase165_goal_only_cutover.py'
)
foreach ($test in $tests) {
  if (-not (Test-Path $test)) { throw "Missing targeted test: $test" }
}
python -m pytest -q @tests
if ($LASTEXITCODE -ne 0) { throw 'R52-R4 targeted pytest failed' }
Write-Host 'R52-R4 targeted tests passed; full pytest NOT run.'
