$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
$package = Join-Path $repo "phase165_r2_repair1"
$source = Join-Path $package "tests\test_phase165_r2_registry_lookup.py"
$target = Join-Path $repo "tests\test_phase165_r2_registry_lookup.py"
if (-not (Test-Path (Join-Path $repo "phase165_r2_registry_lookup.py"))) { throw "R2 implementation missing" }
if (-not (Test-Path $target)) { throw "R2 test target missing" }
Copy-Item $target "$target.phase165_r2_repair1.bak" -Force
Copy-Item $source $target -Force
python -m pytest -q "tests/test_phase165_r2_registry_lookup.py"
if ($LASTEXITCODE -ne 0) { throw "R2 repair1 focused tests failed" }
Write-Host "R2 repair1 focused tests passed. Production files unchanged. Full suite not run."
