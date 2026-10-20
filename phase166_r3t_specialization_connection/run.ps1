$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m pytest -q ".\phase166_r3t_specialization_connection\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m phase166_r3t_specialization_connection.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
