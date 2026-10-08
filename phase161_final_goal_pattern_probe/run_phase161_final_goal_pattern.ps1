$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
$previousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ([string]::IsNullOrEmpty($previousPythonPath)) {
        $repoRoot
    } else {
        "$repoRoot$([IO.Path]::PathSeparator)$previousPythonPath"
    }
    python -B ".\phase161_final_goal_pattern_probe\audit_phase161_final_goal_pattern.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Audit failed with exit code $LASTEXITCODE"
    }
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
