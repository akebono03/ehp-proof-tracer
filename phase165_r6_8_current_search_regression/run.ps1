$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
  $env:PYTHONPATH = "$root;$env:PYTHONPATH"
  python -m pytest -q (Join-Path $PSScriptRoot "test_phase165_r6_8_current_search_regression.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  Write-Host "R6-8 regression PASS; no production files changed; full pytest NOT run."
} finally {
  Pop-Location
}
