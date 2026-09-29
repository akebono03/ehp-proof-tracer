$ErrorActionPreference = "Stop"

python `
  ".\phase143_75m_r3\repair_phase143_75m_r3.py"

$env:PYTHONPATH = (Get-Location).Path

try {
  pytest -q `
    ".\tests\test_phase143_75m_finite_dimensional_semantic_rendering.py"

  python `
    ".\phase143_75m_r2\audit_phase143_75m_r2_target_fallback.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
