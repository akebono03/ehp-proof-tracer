$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
python ".\phase165_r52_r15_ordered_citation\install.py"
if ($LASTEXITCODE -ne 0) { throw 'install failed' }
python -m pytest -q ".\phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py" ".\tests\test_phase164_r2_citation_eligibility.py" ".\test_phase165_r52_r9_shared_math.py"
if ($LASTEXITCODE -ne 0) { throw 'targeted tests failed' }
Write-Host 'R52-R15 targeted checks passed; full pytest NOT run.'
