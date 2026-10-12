$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
$env:PYTHONPATH = "$Project;$PSScriptRoot;$env:PYTHONPATH"
python -m pytest -q ".\phase163_r4_r89_source_assertions\tests\test_phase163_r4_r89_source_assertions.py"
if ($LASTEXITCODE -ne 0) { throw "R89 targeted tests failed" }
python ".\phase163_r4_r89_source_assertions\phase163_r4_r89_source_assertions.py" --r86 ".\phase163_r4_r86_output\claim_review_catalog.json" --r88 ".\phase163_r4_r88_output\scope_conditions.json" --output ".\phase163_r4_r89_output"
if ($LASTEXITCODE -ne 0) { throw "R89 source-only build failed" }
