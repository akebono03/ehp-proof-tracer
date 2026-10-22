$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python ".\phase168_r2_7_given_metadata_guard\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest ".\phase168_r2_7_given_metadata_guard\tests\test_phase168_r2_7_metadata_guard.py" ".\tests\test_phase167_r3_duplicate_given.py" -q
exit $LASTEXITCODE
