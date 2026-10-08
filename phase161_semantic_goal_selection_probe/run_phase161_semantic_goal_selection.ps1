$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
$oldPythonPath = $env:PYTHONPATH
try {
    if ([string]::IsNullOrEmpty($oldPythonPath)) {
        $env:PYTHONPATH = $repoRoot
    } else {
        $env:PYTHONPATH = "$repoRoot$([IO.Path]::PathSeparator)$oldPythonPath"
    }
    python -B ".\phase161_semantic_goal_selection_probe\audit_phase161_semantic_goal_selection.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    $env:PYTHONPATH = $oldPythonPath
}
