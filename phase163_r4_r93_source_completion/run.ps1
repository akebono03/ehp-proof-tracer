$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
$env:PYTHONPATH = $Project
python -m pytest -q ".\phase163_r4_r93_source_completion\tests\test_r93_source_completion.py"
if ($LASTEXITCODE -ne 0) { throw "R93 targeted tests failed" }
python -m phase163_r4_r93_source_completion.r93_source_completion --catalog ".\phase163_r4_r91_output\source_catalog.json" --audit ".\phase163_r4_r92_output\audit.json" --source-dir ".\sources\toda" --output ".\phase163_r4_r93_output"
if ($LASTEXITCODE -ne 0) { throw "R93 completion failed" }
