$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B ".\phase163_r1c_registration_evidence\audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 163 R1C read-only evidence audit finished. Existing source unchanged; full pytest suite not run.'
