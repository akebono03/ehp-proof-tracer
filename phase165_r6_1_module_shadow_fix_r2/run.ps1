$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root
python (Join-Path $PSScriptRoot "apply.py")
if ($LASTEXITCODE -ne 0) { throw "Module synchronization failed" }
python -m pytest -q (Join-Path $PSScriptRoot "test_shadow_fix.py") (Join-Path $Root "phase165_r52_r7_registered_common_proof\test_phase165_r52_r7_registered_common_proof.py")
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
Write-Host "R6-1 module shadow repair complete. Full pytest NOT run."
