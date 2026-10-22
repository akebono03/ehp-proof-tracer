$ErrorActionPreference = "Stop"
$Target = Join-Path (Get-Location).Path "phase167_r4_6_route_trace\test_audit.py"
$Replacement = Join-Path $PSScriptRoot "test_audit.py"
if (-not (Test-Path $Target)) { throw "Original trace test not found" }
Copy-Item -LiteralPath $Target -Destination "$Target.bak" -Force
Copy-Item -LiteralPath $Replacement -Destination $Target -Force
python -m pytest $Target -q
if ($LASTEXITCODE -ne 0) { throw "Trace tests failed" }
Write-Host "Trace tests passed. Existing trace JSON retained."
Write-Host "Production code unchanged. Full pytest not run."
