$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$ProjectRoot;$env:PYTHONPATH" } else { $ProjectRoot }
python -m phase168_r3_22_gap_audit_importfix.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "READ_ONLY: no application sources or tests modified; no full pytest."
