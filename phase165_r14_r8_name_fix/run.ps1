$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r8_source_link.py" ".\phase165_r14_r8_source_link.py" -Force
$OldPath = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($OldPath) { "$Root$([IO.Path]::PathSeparator)$OldPath" } else { $Root }
  python -m pytest -q "$PSScriptRoot\test_phase165_r14_r8_source_link.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python "$PSScriptRoot\audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $OldPath }
Write-Host "Phase 165 R14-R8 targeted checks complete; full pytest NOT run."
