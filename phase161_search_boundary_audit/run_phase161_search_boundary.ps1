$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
python -B ".\phase161_search_boundary_audit\audit_phase161_search_boundary.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
