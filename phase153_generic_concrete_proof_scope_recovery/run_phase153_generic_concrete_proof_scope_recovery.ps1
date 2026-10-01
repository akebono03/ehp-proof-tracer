$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "Phase 153 Generic Concrete Proof-Scope Recovery"
Write-Host "=============================================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_calculation.py"))) {
    throw "Run this script from C:\Users\oomae\Dropbox\Python\fitz\ehp_proof"
}

Write-Host "A. Applying minimal production/test changes..."
python `
  (Join-Path $PackageRoot "apply_phase153_generic_concrete_proof_scope_recovery.py")

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "B. Syntax check..."
python -m py_compile `
  ".\toda_calculation.py" `
  ".\tests\test_phase153_generic_concrete_proof_scope_recovery.py"

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "C. Focused Phase 153 tests..."
python -m pytest `
  ".\tests\test_phase153_generic_concrete_proof_scope_recovery.py" `
  ".\tests\test_phase130_stable_group_specialization.py" `
  -q

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Focused implementation run complete."
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================================="
