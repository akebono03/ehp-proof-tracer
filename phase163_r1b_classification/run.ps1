$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B ".\phase163_r1b_classification\audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 163 R1B read-only classification finished. Source code unchanged; full suite not run.'
