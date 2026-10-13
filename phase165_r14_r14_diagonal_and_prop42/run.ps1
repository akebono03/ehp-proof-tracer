$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r14_diagonal_and_prop42.py" ".\phase165_r14_r14_diagonal_and_prop42.py" -Force
$PreviousPythonPath = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($PreviousPythonPath) { "$Root$([IO.Path]::PathSeparator)$PreviousPythonPath" } else { $Root }
  python -m pytest -q "$PSScriptRoot\test_phase165_r14_r14_diagonal_and_prop42.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python "$PSScriptRoot\audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $PreviousPythonPath }
Write-Host "Phase 165 R14-R14 targeted checks completed; full pytest NOT run."
