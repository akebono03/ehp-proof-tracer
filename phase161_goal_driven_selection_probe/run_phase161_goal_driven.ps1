$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
$original = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ([string]::IsNullOrEmpty($original)) { $repoRoot } else { "$repoRoot$([IO.Path]::PathSeparator)$original" }
    python -B '.\phase161_goal_driven_selection_probe\audit_phase161_goal_driven.py'
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    $env:PYTHONPATH = $original
}
