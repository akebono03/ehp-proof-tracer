$ErrorActionPreference = 'Stop'
python ".\phase165_documentation_closure\update_docs.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 165 documentation closure completed. Full pytest NOT rerun.'
