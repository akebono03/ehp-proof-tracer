$ErrorActionPreference = "Stop"
$repoRoot = (Get-Location).Path
$env:PYTHONPATH = $repoRoot
$scriptPath = Join-Path $PSScriptRoot "audit_phase161_backward_type_closure.py"
python -B $scriptPath
if ($LASTEXITCODE -ne 0) {
    throw "Audit ended without proof success (exit code $LASTEXITCODE); inspect phase161_backward_type_closure_budget_fix.json"
}
