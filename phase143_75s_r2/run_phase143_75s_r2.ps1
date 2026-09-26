$ErrorActionPreference = "Stop"

python `
  ".\phase143_75s_r2\repair_phase143_75s_r2.py"

$env:PYTHONPATH = (Get-Location).Path

try {
  pytest -q `
    ".\tests\test_phase143_75s_toda58_whitehead_square_semantic_rendering.py"

  python `
    ".\phase143_75s\audit_phase143_75s_target_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
