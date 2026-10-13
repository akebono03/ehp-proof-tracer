$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
python (Join-Path $PSScriptRoot "install.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q `
  "test_phase165_r52_r8_show_proof_route.py" `
  "test_phase165_r52_r7_registered_common_proof.py" `
  "test_phase165_r52_r5_auto_search.py" `
  "test_phase165_r52_r4_flask_connection.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R52-R8 targeted tests passed; full pytest NOT run."
