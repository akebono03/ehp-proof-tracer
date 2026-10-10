$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -LiteralPath (Join-Path $package 'phase163_r4_r6_structured_binding.py') -Destination (Join-Path $root 'phase163_r4_r6_structured_binding.py') -Force
Copy-Item -LiteralPath (Join-Path $package 'tests\test_phase163_r4_r6_structured_binding.py') -Destination (Join-Path $root 'tests\test_phase163_r4_r6_structured_binding.py') -Force
python -m pytest -q tests/test_phase163_r4_r6_structured_binding.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 163 R4-R6 focused tests failed' }
Write-Host 'Phase 163 R4-R6 opt-in structured binding focused tests complete. Full suite not run.'
