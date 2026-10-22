$ErrorActionPreference = "Stop"
python -m phase167_r4_6_contribution_identity_audit.audit
if ($LASTEXITCODE -ne 0) { throw "Contribution identity audit failed" }
python -m pytest .\phase167_r4_6_contribution_identity_audit\test_audit.py -q
if ($LASTEXITCODE -ne 0) { throw "Contribution identity tests failed" }
Write-Host "Production code unchanged; full pytest not run."
