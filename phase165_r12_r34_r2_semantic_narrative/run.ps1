$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$project$([IO.Path]::PathSeparator)$env:PYTHONPATH"
python "$folder\install.py"
if ($LASTEXITCODE -ne 0) { throw "Install failed" }
python -m pytest -q "$folder\test_r12_r34_r2.py"
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }
python "$folder\audit.py"
if ($LASTEXITCODE -ne 0) { throw "Audit failed" }
