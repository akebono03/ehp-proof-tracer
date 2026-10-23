$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot
python (Join-Path $PSScriptRoot "audit.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "READ_ONLY: no application sources or tests modified; no full pytest."
