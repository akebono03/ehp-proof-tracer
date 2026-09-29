$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ab3\apply_phase143_75ab3.py"

  pytest -q `
    ".\tests\test_phase60_nu4_whitehead_correction.py" `
    ".\tests\test_phase143_75ab3_whitehead_correction_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
