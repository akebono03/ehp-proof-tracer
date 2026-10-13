$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'web_group_proof.py'))) { throw 'Run this script from the repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R52-R3 installation failed' }
python -m pytest -q (Join-Path $root 'test_phase165_r52_r3_web_adapter.py') (Join-Path $root 'test_phase165_r52_partial_proof.py') (Join-Path $root 'test_phase165_r52_r2_search_adapter.py') (Join-Path $root 'test_phase165_r52_r2_engine_observer.py') (Join-Path $root 'tests/test_phase165_r3_recursive_search.py') (Join-Path $root 'tests/test_phase165_r9_production_wiring.py') (Join-Path $root 'tests/test_phase165_goal_only_cutover.py')
if ($LASTEXITCODE -ne 0) { throw 'R52-R3 targeted pytest failed' }
Write-Host 'R52-R3 common Web view adapter passed targeted tests; full pytest NOT run.'
