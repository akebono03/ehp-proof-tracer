$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
$env:PYTHONPATH = $Project
python -m pytest -q ".\phase163_r4_r92_gap_completion\tests\test_phase163_r4_r92_gap_completion.py"
if ($LASTEXITCODE -ne 0) { throw "R92 targeted tests failed" }
python ".\phase163_r4_r92_gap_completion\phase163_r4_r92_gap_completion.py" --catalog ".\phase163_r4_r91_output\source_catalog.json" --source-dir ".\sources\toda" --output ".\phase163_r4_r92_output"
if ($LASTEXITCODE -ne 0) { throw "R92 source-only audit/registration failed" }
