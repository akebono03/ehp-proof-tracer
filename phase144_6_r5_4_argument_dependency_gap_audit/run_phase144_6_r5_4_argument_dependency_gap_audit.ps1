$ErrorActionPreference = "Stop"

$env:PYTHONPATH = (Get-Location).Path

try {
  python ".\phase144_6_r5_4_argument_dependency_gap_audit\audit_phase144_6_r5_4_argument_dependency_gap.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
