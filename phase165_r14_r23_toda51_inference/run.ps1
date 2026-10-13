$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r23_toda51_inference.py" ".\phase165_r14_r23_toda51_inference.py" -Force
$Previous = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($Previous) { "$Root$([IO.Path]::PathSeparator)$Previous" } else { $Root }
  python -m pytest -q "$PSScriptRoot\test_phase165_r14_r23_toda51_inference.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python "$PSScriptRoot\audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $Previous }
Write-Host "R14-R23 targeted tests complete; full pytest NOT run."
