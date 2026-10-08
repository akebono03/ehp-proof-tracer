$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$previousPythonPath = $env:PYTHONPATH
Push-Location $repoRoot
try {
    $env:PYTHONPATH = if ([string]::IsNullOrEmpty($previousPythonPath)) {
        $repoRoot
    } else {
        "$repoRoot$([IO.Path]::PathSeparator)$previousPythonPath"
    }
    python -B (Join-Path $PSScriptRoot "audit_phase161_concrete_goal_filter.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Concrete goal audit failed with exit code $LASTEXITCODE"
    }
} finally {
    $env:PYTHONPATH = $previousPythonPath
    Pop-Location
}
