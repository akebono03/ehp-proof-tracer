$ErrorActionPreference = "Stop"

$env:PYTHONPATH = (Get-Location).Path

try {
  python `
    ".\phase143_75k\audit_phase143_75k_finite_group_semantic_structure.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
