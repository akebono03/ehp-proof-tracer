$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = $PSScriptRoot
$env:PYTHONPATH = $root
python -B (Join-Path $package "apply_phase162_r4_b3_web_common_display.py")
if ($LASTEXITCODE -ne 0) { throw "Patch failed." }
Copy-Item (Join-Path $package "files\tests\test_phase162_r4_b3_web_common_display.py") (Join-Path $root "tests\test_phase162_r4_b3_web_common_display.py") -Force
python -B -m pytest -q tests/test_phase162_r4_b3_web_common_display.py
if ($LASTEXITCODE -ne 0) { throw "Focused tests failed." }
Write-Host "R4-B3 derived proof now routed to Web Group Proof narrative for pi_5^4 and pi_6^5. Full suite not run."
