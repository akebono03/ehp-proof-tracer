$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'web_app.py'))) { throw 'Run from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R52-R5 installation failed' }
$testPaths = @(
  'test_phase165_r52_r5_auto_search.py'
  'test_phase165_r52_partial_proof.py'
  'test_phase165_r52_r2_search_adapter.py'
  'test_phase165_r52_r2_engine_observer.py'
  'test_phase165_r52_r3_web_adapter.py'
  'test_phase165_r52_r3_empty_steps_contract.py'
  'test_phase165_r52_r4_flask_connection.py'
  'tests/test_phase165_r3_recursive_search.py'
  'tests/test_phase165_r9_production_wiring.py'
  'tests/test_phase165_goal_only_cutover.py'
)
foreach ($p in $testPaths) {
  if (-not (Test-Path (Join-Path $root $p))) { throw "Missing targeted test: $p" }
}
$absolutePaths = @($testPaths | ForEach-Object { Join-Path $root $_ })
python -m pytest -q @absolutePaths
if ($LASTEXITCODE -ne 0) { throw 'R52-R5 targeted pytest failed' }
Write-Host 'R52-R5 targeted tests passed; full pytest NOT run.'
