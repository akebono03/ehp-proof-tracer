$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146-2 Structural Capability Diagnosis"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile "$ScriptDir\diagnose_phase146_2.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Syntax preflight failed."
    }

    Write-Host ""
    Write-Host "B. Comparing six current Narrative structures..."
    python "$ScriptDir\diagnose_phase146_2.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 146-2 diagnosis failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
