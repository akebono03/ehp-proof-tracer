$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R1 repair1 - audit runtime + UTF-8 repair"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path
$OutputDir = Join-Path $PackageDir "output"

Set-Location $RepoRoot

$OldPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrEmpty($OldPythonPath)) {
    $env:PYTHONPATH = $RepoRoot
}
else {
    $env:PYTHONPATH = "$RepoRoot;$OldPythonPath"
}

try {
    Remove-Item `
      $OutputDir `
      -Recurse `
      -Force `
      -ErrorAction SilentlyContinue

    Write-Host "[1/3] Focused audit-runtime tests"
    python -m pytest `
      ".\phase158_r1_repair1_audit_runtime\test_phase158_r1_repair1.py" `
      -q

    Write-Host "[2/3] 112-group public-contract inventory"
    python `
      ".\phase158_r1_repair1_audit_runtime\audit_phase158_r1_repair1.py"

    Write-Host "[3/3] Show UTF-8 summary"
    Get-Content `
      ".\phase158_r1_repair1_audit_runtime\output\narrative_public_contract_summary.txt" `
      -Encoding UTF8
}
finally {
    $env:PYTHONPATH = $OldPythonPath
}

Write-Host "=============================================================="
Write-Host "Phase 158-R1 repair1 complete."
Write-Host "Production code changes: none"
Write-Host "Full repository pytest: NOT run in R1"
Write-Host "=============================================================="
