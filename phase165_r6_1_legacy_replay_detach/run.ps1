$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
python (Join-Path $PSScriptRoot "apply.py")
if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
python -m pytest -q (Join-Path $PSScriptRoot "test_detach.py")
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "Old R40/R41 reconstruction detached. Full pytest NOT run."
