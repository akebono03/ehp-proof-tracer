$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================="
Write-Host "Phase 153-R2 Follow-up Audit"
Write-Host "Reference-only / Reference + Semantic Fact / Unresolved"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_group_proof_narrative_renderer.py"))) {
  throw "Run this script from C:\Users\oomae\Dropbox\Python\fitz\ehp_proof"
}

Write-Host "A. Syntax check..."
python -m py_compile `
  (Join-Path $PackageRoot "audit_phase153_r2_reference_semantic_fact.py")
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "B. Running 112-group audit..."
python `
  (Join-Path $PackageRoot "audit_phase153_r2_reference_semantic_fact.py") `
  2>&1 | Tee-Object `
  -FilePath (Join-Path $PackageRoot "audit_run_output.txt")
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit complete."
Write-Host "Production files were NOT changed."
Write-Host "Full pytest was NOT run."
Write-Host ""
Write-Host "Please paste audit_run_output.txt or the console summary."
Write-Host "=============================================================="
