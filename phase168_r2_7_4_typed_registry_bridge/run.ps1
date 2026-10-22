$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot
python ".\phase168_r2_7_4_typed_registry_bridge\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase168_r2_7_4_typed_registry_bridge\tests\test_literature_connection.py" ".\tests\test_phase167_r3_duplicate_given.py" ".\tests\test_phase163_r4_r11_literature_registration.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
