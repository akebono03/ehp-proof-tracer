$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r22_same_reference.py" ".\phase165_r14_r22_same_reference.py" -Force
$Old = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($Old) { "$Root$([IO.Path]::PathSeparator)$Old" } else { $Root }
  python -m pytest -q "$PSScriptRoot\test_phase165_r14_r22_same_reference.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python "$PSScriptRoot\audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $Old }
Write-Host "R14-R22 targeted only; full pytest NOT run."
