$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ad_impl\repair_phase143_75ad.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Copy-Item `
    ".\phase143_75ad_impl\test_phase143_75ad_double_suspension_rendering.py" `
    ".\tests\test_phase143_75ad_double_suspension_rendering.py" `
    -Force

  pytest -q `
    ".\tests\test_phase60_toda36_specialization.py" `
    ".\tests\test_phase143_75ad_double_suspension_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
