$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python ".\phase165_prop51_literature_r6\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase165_prop51_literature_r6\test_prop51_literature.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Prop 5.1 literature registration targeted tests passed; full pytest NOT run.'
