$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$DiagSource = Join-Path $PatchRoot "diagnose_phase144_6_pi16_9_ordering.py"
$DiagTarget = Join-Path $ProjectRoot "diagnose_phase144_6_pi16_9_ordering.py"

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Diagnosis R6"
Write-Host "pi_16^9 compact ordering diagnosis"
Write-Host "Production code changes: none"
Write-Host "Persistent test changes: none"
Write-Host "=============================================================="

Copy-Item -Path $DiagSource -Destination $DiagTarget -Force
$env:PYTHONPATH = $ProjectRoot

try {
  python $DiagTarget
  if ($LASTEXITCODE -ne 0) {
    throw "Compact diagnosis failed."
  }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item $DiagTarget -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Diagnosis complete."
Write-Host "Please paste the complete output."
