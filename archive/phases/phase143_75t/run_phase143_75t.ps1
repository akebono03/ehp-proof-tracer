$ErrorActionPreference = "Stop"

python `
  ".\phase143_75t\repair_phase143_75t.py"

python `
  ".\phase143_75t\install_phase143_75t_test.py"

$env:PYTHONPATH = (Get-Location).Path

try {
  pytest -q `
    ".\tests\test_phase143_75t_toda58_equation_aggregate_semantic_rendering.py"

  python `
    ".\phase143_75t\audit_phase143_75t_aggregate_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
