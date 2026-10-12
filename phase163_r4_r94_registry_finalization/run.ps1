$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
$env:PYTHONPATH = $Project
python -m pytest -q ".\phase163_r4_r94_registry_finalization\tests\test_r94_registry_finalization.py"
if ($LASTEXITCODE -ne 0) { throw "R94 targeted tests failed" }
python -m phase163_r4_r94_registry_finalization.r94_registry_finalization --catalog ".\phase163_r4_r91_output\source_catalog.json" --audit ".\phase163_r4_r92_output\audit.json" --source-dir ".\sources\toda" --output ".\phase163_r4_r94_output"
if ($LASTEXITCODE -ne 0) { throw "R94 manifest finalization failed" }
