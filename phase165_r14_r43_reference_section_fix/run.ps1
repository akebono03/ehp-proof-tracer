$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python (Join-Path $PSScriptRoot "install.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$Previous = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($Previous) { "$Root$([IO.Path]::PathSeparator)$Previous" } else { $Root }
  python -m pytest -q (Join-Path $PSScriptRoot "test_phase165_r14_r43_reference_reason.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $Previous }
Write-Host "R43 targeted tests passed; full pytest NOT run. Restart Web server."
