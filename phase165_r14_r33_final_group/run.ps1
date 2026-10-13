$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r33_final_group.py" ".\phase165_r14_r33_final_group.py" -Force
$Previous = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($Previous) { "$Root$([IO.Path]::PathSeparator)$Previous" } else { $Root }
  python -m pytest -q "$PSScriptRoot\test_phase165_r14_r33_final_group.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python "$PSScriptRoot\audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $Previous }
Write-Host "R14-R33 targeted tests complete; full pytest NOT run."
