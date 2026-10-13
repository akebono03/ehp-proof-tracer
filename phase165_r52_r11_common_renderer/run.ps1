$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
python (Join-Path $PSScriptRoot "install.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q `
  "test_phase165_r52_r11_common_renderer.py" `
  "test_phase165_r52_r10_readable_partial.py" `
  "test_phase165_r52_partial_proof.py" `
  "test_phase165_r52_r9_shared_math.py" `
  "test_phase165_r52_r8_show_proof_route.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R52-R11 targeted tests passed; full pytest NOT run."
