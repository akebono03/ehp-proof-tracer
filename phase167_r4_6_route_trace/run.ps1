$ErrorActionPreference = "Stop"
python -m phase167_r4_6_route_trace.audit
if ($LASTEXITCODE -ne 0) { throw "Runtime trace failed" }
python -m pytest .\phase167_r4_6_route_trace\test_audit.py -q
if ($LASTEXITCODE -ne 0) { throw "Trace self-tests failed" }
Write-Host "Production code unchanged; full pytest not run."
