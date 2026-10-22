$ErrorActionPreference = "Stop"
python ".\phase167_r4_9_dependency_audit\audit.py"
if ($LASTEXITCODE -ne 0) { throw "Audit failed" }
Write-Host "Read-only audit completed. No production files modified."
