$ErrorActionPreference = "Stop"
python -m phase167_r4_6_stage_origin_audit.audit
if ($LASTEXITCODE -ne 0) { throw "Stage-origin audit failed" }
python -m pytest .\phase167_r4_6_stage_origin_audit\test_audit.py -q
if ($LASTEXITCODE -ne 0) { throw "Stage-origin tests failed" }
Write-Host "No production changes. Full pytest not run."
