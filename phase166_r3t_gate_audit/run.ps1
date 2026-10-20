$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m pytest -q ".\phase166_r3t_gate_audit\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m phase166_r3t_gate_audit.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
