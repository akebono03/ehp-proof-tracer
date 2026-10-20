$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m pytest -q ".\phase166_r3t_search_boundary\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m phase166_r3t_search_boundary.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
