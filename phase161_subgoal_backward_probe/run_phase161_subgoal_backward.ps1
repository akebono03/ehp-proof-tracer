$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONPATH = $root
Push-Location $root
try {
    python -B (Join-Path $PSScriptRoot 'audit_phase161_subgoal_backward.py')
    if ($LASTEXITCODE -ne 0) { throw "Audit failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
