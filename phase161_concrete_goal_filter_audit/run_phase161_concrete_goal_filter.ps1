$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    python -B (Join-Path $PSScriptRoot "audit_phase161_concrete_goal_filter.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Concrete goal audit failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}
