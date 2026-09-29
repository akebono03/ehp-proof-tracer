$ErrorActionPreference = "Stop"

python `
  ".\phase143_75p\repair_phase143_75p.py"

Copy-Item `
  ".\phase143_75p\test_phase143_75p_prop44_suspension_injective_semantic_rendering.py" `
  ".\tests\test_phase143_75p_prop44_suspension_injective_semantic_rendering.py" `
  -Force

$env:PYTHONPATH = (Get-Location).Path

try {
  pytest -q `
    ".\tests\test_phase143_75p_prop44_suspension_injective_semantic_rendering.py"

  python `
    ".\phase143_75p\audit_phase143_75p_target_fallback.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
