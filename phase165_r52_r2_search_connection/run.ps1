$ErrorActionPreference = 'Stop'
python ".\phase165_r52_r2_search_connection\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R52-R2 installation failed' }
python -m pytest -q test_phase165_r52_partial_proof.py test_phase165_r52_r2_search_adapter.py test_phase165_r52_r2_engine_observer.py tests/test_phase165_r3_recursive_search.py tests/test_phase165_r9_production_wiring.py tests/test_phase165_goal_only_cutover.py
if ($LASTEXITCODE -ne 0) { throw 'R52-R2 targeted pytest failed' }
Write-Host 'R52-R2 observer/adapter installed; full pytest NOT run.'
