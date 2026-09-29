$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146-1 pi_6^3 Public Narrative Route Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="
Write-Host ""

$RepoRoot = (Get-Location).Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host "A. Syntax preflight..."
    python -m py_compile "$ScriptDir\audit_phase146_1.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Syntax preflight failed."
    }

    Write-Host ""
    Write-Host "B. Running Phase 146-1 audit..."
    python "$ScriptDir\audit_phase146_1.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 146-1 audit failed."
    }

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 146-1 audit: PASS"
    Write-Host "Next boundary: Phase 146-2 may repair only the confirmed route gate."
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
