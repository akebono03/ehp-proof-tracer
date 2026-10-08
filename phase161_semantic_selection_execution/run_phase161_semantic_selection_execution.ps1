$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$env:PYTHONPATH = $repositoryRoot
Push-Location $repositoryRoot
try {
    python -B (Join-Path $PSScriptRoot "audit_phase161_semantic_selection_execution.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Audit failed with exit code $LASTEXITCODE; see phase161_semantic_selection_execution.json"
    }
} finally {
    Pop-Location
}
