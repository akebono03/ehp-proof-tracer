$ErrorActionPreference = "Stop"
python -B ".\phase161_depth_comparison_audit\audit_phase161_depth_comparison.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
