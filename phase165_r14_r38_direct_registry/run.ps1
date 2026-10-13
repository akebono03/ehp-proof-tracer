$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r3_recursive_search.py" ".\phase165_r3_recursive_search.py" -Force
Copy-Item "$PSScriptRoot\phase165_r14_r38_direct_registry.py" ".\phase165_r14_r38_direct_registry.py" -Force
$Old = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($Old) { "$Root$([IO.Path]::PathSeparator)$Old" } else { $Root }
  python -m pytest -q "$PSScriptRoot\test_phase165_r14_r38_direct_registry.py" "tests/test_phase165_r3_recursive_search.py" "tests/test_phase165_r2_registry_lookup.py"
  if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed; full suite NOT run." }
  python "$PSScriptRoot\audit.py"
  if ($LASTEXITCODE -ne 0) { throw "Audit failed; full suite NOT run." }
  Write-Host "Registered typed-reference proof passed. Running full pytest at phase closure."
  python -m pytest -q
  if ($LASTEXITCODE -ne 0) { throw "Full pytest failed; phase not closed." }
  Write-Host "Phase 165 goal and full pytest complete."
} finally {
  $env:PYTHONPATH = $Old
}
