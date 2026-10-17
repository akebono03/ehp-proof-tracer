$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$project$([IO.Path]::PathSeparator)$env:PYTHONPATH"
python "$folder\install.py"
if ($LASTEXITCODE -ne 0) { throw "install failed" }
python -m pytest -q "$folder\test_phase165_r12_r34_narrative.py"
if ($LASTEXITCODE -ne 0) { throw "tests failed" }
python "$folder\audit.py"
if ($LASTEXITCODE -ne 0) { throw "audit failed" }
