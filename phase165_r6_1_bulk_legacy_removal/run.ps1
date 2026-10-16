$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
python (Join-Path $PSScriptRoot "apply.py")
if ($LASTEXITCODE -ne 0) { throw "Removal failed" }
python -m pytest -q (Join-Path $PSScriptRoot "test_after_removal.py")
if ($LASTEXITCODE -ne 0) { throw "Focused regression failed" }
Write-Host "Legacy R37/R40/R41 root paths removed; full pytest NOT run."
