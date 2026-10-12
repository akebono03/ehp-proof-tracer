$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item (Join-Path $PackageDir 'phase165_r3_recursive_search.py') (Join-Path $Root 'phase165_r3_recursive_search.py') -Force
$Boundary = Join-Path $Root 'phase165_goal_only_search.py'
if (-not (Test-Path $Boundary)) { throw 'Phase 165 R1 boundary not installed' }
Copy-Item $Boundary ($Boundary + '.phase165_r3_backup') -Force
Copy-Item (Join-Path $PackageDir 'phase165_goal_only_search.py') $Boundary -Force
Copy-Item (Join-Path $PackageDir 'tests\test_phase165_r3_recursive_search.py') (Join-Path $Root 'tests\test_phase165_r3_recursive_search.py') -Force
python -m py_compile '.\phase165_goal_only_search.py' '.\phase165_r3_recursive_search.py' '.\tests\test_phase165_r3_recursive_search.py'
if ($LASTEXITCODE -ne 0) { throw 'R3 syntax check failed' }
python -m pytest -q '.\tests\test_phase165_r3_recursive_search.py' '.\tests\test_phase165_r2_registry_lookup.py'
if ($LASTEXITCODE -ne 0) { throw 'R3 focused tests failed' }
Write-Host 'R3 generic recursive search installed. Goal-only production discovery is not yet complete; no full suite run.'
