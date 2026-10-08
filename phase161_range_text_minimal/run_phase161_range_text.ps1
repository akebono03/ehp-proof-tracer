$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B ".\phase161_range_text_minimal\apply_phase161_range_text.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest -q ".\phase161_range_text_minimal\test_phase161_range_text.py"
exit $LASTEXITCODE
