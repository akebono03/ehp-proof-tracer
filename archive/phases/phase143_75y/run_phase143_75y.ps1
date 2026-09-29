$ErrorActionPreference = "Stop"

python `
  ".\phase143_75y\repair_phase143_75y.py"

python `
  ".\phase143_75y\install_phase143_75y_test.py"

$env:PYTHONPATH = (Get-Location).Path

try {
  pytest -q `
    ".\tests\test_phase143_75y_nu4_construction_semantic_rendering.py"

  python `
    ".\phase143_75y\audit_phase143_75y_nu4_construction_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
