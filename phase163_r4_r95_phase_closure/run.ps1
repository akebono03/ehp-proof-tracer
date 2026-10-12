$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
$env:PYTHONPATH = $Project

# Explicitly selected tests only. NEVER run pytest without test paths.
python -m pytest -q `
  ".\phase163_r4_r95_phase_closure\tests\test_r95_phase_closure.py" `
  ".\phase163_r4_r94_registry_finalization\tests\test_r94_registry_finalization.py" `
  ".\tests\test_phase163_r2_unified_registry.py" `
  ".\tests\test_phase163_r4_registry_bridge.py"
if ($LASTEXITCODE -ne 0) { throw "R95 targeted tests failed" }

python -m phase163_r4_r95_phase_closure.r95_phase_closure `
  --manifest ".\phase163_r4_r94_output\manifest.json" `
  --catalog ".\phase163_r4_r91_output\source_catalog.json" `
  --audit ".\phase163_r4_r92_output\audit.json" `
  --source-dir ".\sources\toda" `
  --output ".\phase163_r4_r95_output"
if ($LASTEXITCODE -ne 0) { throw "R95 closure audit failed" }
Write-Output "R95 targeted-only closure completed; full pytest was NOT run."
