$ErrorActionPreference = "Stop"

python `
  ".\phase143_75m\apply_phase143_75m.py"

$env:PYTHONPATH = (Get-Location).Path

try {
  pytest -q `
    ".\tests\test_phase143_75m_finite_dimensional_semantic_rendering.py"

  python `
    ".\phase143_75m\audit_phase143_75m_target_fallback.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
