$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
python ".\phase165_unification_audit\audit.py"
if ($LASTEXITCODE -ne 0) { throw "Phase 165 unification audit failed" }
Write-Host "Phase 165: audit complete; production files unchanged; full pytest NOT run."
