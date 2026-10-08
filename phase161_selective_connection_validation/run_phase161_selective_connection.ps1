$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ([string]::IsNullOrEmpty($oldPythonPath)) {
        $repoRoot
    } else {
        "$repoRoot$([IO.Path]::PathSeparator)$oldPythonPath"
    }
    python -B ".\phase161_selective_connection_validation\audit_phase161_selective_connection.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    $env:PYTHONPATH = $oldPythonPath
}
