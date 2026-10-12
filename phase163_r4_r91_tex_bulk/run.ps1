$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$Project;$env:PYTHONPATH" } else { $Project }
python -m pytest -q ".\phase163_r4_r91_tex_bulk\tests\test_phase163_r4_r91_tex_bulk.py"
if ($LASTEXITCODE -ne 0) { throw "R91 targeted tests failed" }
python -m phase163_r4_r91_tex_bulk.phase163_r4_r91_tex_bulk --source-dir ".\sources\toda" --output ".\phase163_r4_r91_output"
if ($LASTEXITCODE -ne 0) { throw "R91 source registration failed" }
