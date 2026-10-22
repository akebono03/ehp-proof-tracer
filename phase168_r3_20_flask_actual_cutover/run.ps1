$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
python (Join-Path $PSScriptRoot "patch.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $PSScriptRoot "tests\test_phase168_r3_20_flask_actual_cutover.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $Project "phase168_r3_6_standard_web_entry\tests\test_phase168_r3_6_standard_web_entry.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Flask entry model cutover checked. Full pytest deferred to Phase 168 end."
