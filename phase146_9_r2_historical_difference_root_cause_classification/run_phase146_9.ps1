$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146-9 Historical Difference Root-Cause Classification"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Phase1468Report = Join-Path $RepoRoot "phase146_8_historical_narrative_structural_diff.md"
$Report = Join-Path $RepoRoot "phase146_9_historical_difference_root_causes.md"

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Checking Phase 146-8 input..."
    if (-not (Test-Path $Phase1468Report)) {
        throw "Missing Phase 146-8 report: $Phase1468Report"
    }

    Write-Host ""
    Write-Host "B. Syntax preflight..."
    python -m py_compile "$ScriptDir\audit_phase146_9.py"
    if ($LASTEXITCODE -ne 0) { throw "Syntax preflight failed." }

    Write-Host ""
    Write-Host "C. Running pi_6^3 argument / exactness / contribution diagnostics..."
    python "$ScriptDir\audit_phase146_9.py" `
      $Phase1468Report `
      $Report
    if ($LASTEXITCODE -ne 0) { throw "Phase 146-9 audit failed." }

    Write-Host ""
    Write-Host "D. UTF-8 integrity check..."
    python -c "from pathlib import Path; Path(r'$Report').read_text(encoding='utf-8', errors='strict'); print('UTF-8 strict decode: PASS')"
    if ($LASTEXITCODE -ne 0) { throw "UTF-8 integrity check failed." }

    Write-Host ""
    Write-Host "E. Audit artifact..."
    Write-Host "   $Report"
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 146-9 audit complete."
Write-Host "Production changes: none"
Write-Host "Full pytest suite intentionally not run."
Write-Host "=============================================================="
