$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r27_scope_delta.py" ".\phase165_r14_r27_scope_delta.py" -Force
$Old = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($Old) { "$Root$([IO.Path]::PathSeparator)$Old" } else { $Root }
  python -m pytest -q "$PSScriptRoot\test_phase165_r14_r27_scope_delta.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  if (Test-Path ".\Toda_01.tex") {
    python "$PSScriptRoot\audit.py" ".\Toda_01.tex"
  } else {
    python "$PSScriptRoot\audit.py"
  }
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $Old }
Write-Host "R14-R27 targeted checks finished; full pytest NOT run."
