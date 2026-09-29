$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Get-Location).Path

try {
  python ".\phase143_75aa_r2\apply_phase143_75aa_r2.py"

  pytest -q `
    ".\tests\test_phase63_nu4_prop44_specialization.py" `
    ".\tests\test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
