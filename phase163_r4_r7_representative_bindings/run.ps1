$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
$package = $PSScriptRoot
$required = @(
  "unified_statement_registry.py",
  "phase163_r4_registry_bridge.py",
  "phase163_r4_r6_structured_binding.py",
  "phase162_reference_boundary.py",
  "probes\probe_phase58_capabilities.py",
  "probes\probe_phase65_capabilities.py"
)
foreach ($relative in $required) {
  if (-not (Test-Path (Join-Path $project $relative))) {
    throw "Required existing project file missing: $relative"
  }
}
$dest = Join-Path $project "tests"
if (-not (Test-Path $dest)) { throw "Project tests directory missing" }
Copy-Item (Join-Path $package "phase163_r4_r7_representative_bindings.py") (Join-Path $project "phase163_r4_r7_representative_bindings.py") -Force
Copy-Item (Join-Path $package "tests\test_phase163_r4_r7_representative_bindings.py") (Join-Path $dest "test_phase163_r4_r7_representative_bindings.py") -Force
python -m pytest -q tests/test_phase163_r4_r6_structured_binding.py tests/test_phase163_r4_r7_representative_bindings.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
python phase163_r4_r7_representative_bindings.py
if ($LASTEXITCODE -ne 0) { throw "Representative binding audit failed: $LASTEXITCODE" }
Write-Host "Phase 163 R4-R7 focused tests and representative audit finished. Full suite not run."
