$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
Write-Host 'Phase 164 R9-R2 inline TeX duplicate sequence correction'
python (Join-Path $PSScriptRoot 'apply.py') --root . --dry-run
if ($LASTEXITCODE -ne 0) { throw 'Preflight failed; production unchanged' }
python (Join-Path $PSScriptRoot 'apply.py') --root .
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R9-R2 failed; see diagnostic output' }
Write-Host 'R9-R2 targeted and live pi_5^3 check PASS; full pytest NOT run.'
