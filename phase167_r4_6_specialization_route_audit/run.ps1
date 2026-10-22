$ErrorActionPreference = "Stop"
python -m phase167_r4_6_specialization_route_audit.audit
if ($LASTEXITCODE -ne 0) { throw "R4-6 audit failed" }
python -m pytest .\phase167_r4_6_specialization_route_audit\test_audit.py -q
if ($LASTEXITCODE -ne 0) { throw "R4-6 limited pytest failed" }
Write-Host "Full pytest not run; production code not modified."
