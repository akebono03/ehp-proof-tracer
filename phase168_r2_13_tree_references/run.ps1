$ErrorActionPreference = "Stop"
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
python -m pytest -q "$dir\tests\test_phase168_r2_13_patch.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$dir\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q tests/test_phase167_r2_shared_reference.py tests/test_phase167_r2_unified_reference.py
if ($LASTEXITCODE -ne 0) { Write-Host "LIMITED_TESTS_FAILED: restore from output backup"; exit $LASTEXITCODE }
Write-Host "LIMITED_TESTS_PASSED"
