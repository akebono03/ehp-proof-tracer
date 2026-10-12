$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
$package = Join-Path $repo "phase165_r2_registry_lookup"
Copy-Item (Join-Path $package "phase165_r2_registry_lookup.py") (Join-Path $repo "phase165_r2_registry_lookup.py") -Force
$dest = Join-Path $repo "tests\test_phase165_r2_registry_lookup.py"
Copy-Item (Join-Path $package "tests\test_phase165_r2_registry_lookup.py") $dest -Force
python -m pytest -q "tests/test_phase165_r2_registry_lookup.py"
if ($LASTEXITCODE -ne 0) { throw "R2 focused tests failed" }
Write-Host "R2 registry lookup installed. Goal-only full proof search is still incomplete. Full suite not run."
