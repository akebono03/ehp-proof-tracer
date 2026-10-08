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
    python -B ".\phase161_binding_propagation_probe\audit_phase161_binding_propagation.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
