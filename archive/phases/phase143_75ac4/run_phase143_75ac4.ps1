$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ac4\repair_phase143_75ac4.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Copy-Item `
    ".\phase143_75ac4\test_phase143_75ac4_hopf_odd_multiple_rendering.py" `
    ".\tests\test_phase143_75ac4_hopf_odd_multiple_rendering.py" `
    -Force

  pytest -q `
    ".\tests\test_phase60_toda48_hopf_parity.py" `
    ".\tests\test_phase143_75ac4_hopf_odd_multiple_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
