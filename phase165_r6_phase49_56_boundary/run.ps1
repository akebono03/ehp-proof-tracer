$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python ".\phase165_r6_phase49_56_boundary\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'Phase49/56 inventory failed' }
python -m pytest -q ".\phase165_r6_phase49_56_boundary\test_current_boundary.py"
if ($LASTEXITCODE -ne 0) { throw 'Phase49/56 modern boundary tests failed' }
Write-Host 'Phase49/56 current boundary PASS; legacy mathematical equivalence NOT verified; full pytest NOT run.'
