$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repositoryRoot
$previousPythonPath = $env:PYTHONPATH
try {
    if ([string]::IsNullOrEmpty($previousPythonPath)) {
        $env:PYTHONPATH = $repositoryRoot
    } else {
        $env:PYTHONPATH = $repositoryRoot + [System.IO.Path]::PathSeparator + $previousPythonPath
    }
    Write-Host "Repository root: $repositoryRoot"
    Write-Host "=== E2 eta3 dependency audit (read-only) ==="
    python -B (Join-Path $PSScriptRoot "audit_phase162_e2_dependency.py")
    if ($LASTEXITCODE -ne 0) { throw "Dependency audit failed (exit code $LASTEXITCODE)" }
    Write-Host "Phase 162 R5-6 dependency audit complete. No files changed; full suite not run."
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
