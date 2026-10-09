$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest -q "$PSScriptRoot\test_r10_r7.py" "tests\test_phase162_r4_b_common_renderer_link.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R10-R7 focused tests complete. Full suite not run.'
