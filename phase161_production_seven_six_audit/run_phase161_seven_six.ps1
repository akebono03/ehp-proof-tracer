$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
$oldPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ([string]::IsNullOrEmpty($oldPath)) { $repoRoot } else { "$repoRoot$([IO.Path]::PathSeparator)$oldPath" }
    python -B '.\phase161_production_seven_six_audit\audit_phase161_seven_six.py'
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    $env:PYTHONPATH = $oldPath
}
