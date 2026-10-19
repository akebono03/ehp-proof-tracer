$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
  python (Join-Path $PSScriptRoot "apply.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python -m pytest -q phase165_r57_r1_single_entry/test_phase165_r57_r1_single_entry.py
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  Write-Host "R57-R1 targeted pytest passed. Full pytest was NOT run."
} finally {
  Pop-Location
}
