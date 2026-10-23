$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
python (Join-Path $PSScriptRoot "patch.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $PSScriptRoot "tests\test_phase168_r3_21_ehp_exactness_prose.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Focused test complete; entire suite deferred to end of Phase 168."
