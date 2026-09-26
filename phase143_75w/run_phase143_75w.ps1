$ErrorActionPreference = "Stop"

python `
  ".\phase143_75w\repair_phase143_75w.py"

python `
  ".\phase143_75w\install_phase143_75w_test.py"

$env:PYTHONPATH = (Get-Location).Path

try {
  pytest -q `
    ".\tests\test_phase143_75w_toda54_bracket_up_to_sign_semantic_rendering.py"

  python `
    ".\phase143_75w\audit_phase143_75w_toda54_bracket_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
