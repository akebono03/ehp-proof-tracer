$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
python (Join-Path $PSScriptRoot "patch.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $PSScriptRoot "tests\test_phase168_r3_19_web_model_default.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $Project "phase168_r3_6_standard_web_entry\tests\test_phase168_r3_6_standard_web_entry.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Limited validation completed. Phase 168 full suite not run."
