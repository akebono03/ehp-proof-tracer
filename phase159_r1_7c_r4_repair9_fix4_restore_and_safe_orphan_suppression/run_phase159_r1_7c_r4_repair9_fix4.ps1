$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$PreviousPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = "$RepoRoot;$PreviousPythonPath"
}

try {
  Write-Host "=============================================================="
  Write-Host "Phase 159 R1-7c R4 repair9 fix4"
  Write-Host "restore + syntax-safe orphan suppression"
  Write-Host "=============================================================="
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/6] Restore fix3 backup and apply fix4"
  python ".\phase159_r1_7c_r4_repair9_fix4_restore_and_safe_orphan_suppression\apply_phase159_r1_7c_r4_repair9_fix4.py"
  if ($LASTEXITCODE -ne 0) {
    throw "fix4 apply failed."
  }

  Write-Host ""
  Write-Host "[2/6] Syntax compile"
  python -m py_compile ".\toda_group_proof_narrative_contribution_renderer.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Syntax compile failed."
  }

  Write-Host ""
  Write-Host "[3/6] Targeted audit"
  python ".\phase159_r1_7c_r4_repair9_fix4_restore_and_safe_orphan_suppression\audit_phase159_r1_7c_r4_repair9_fix4.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Targeted audit failed."
  }

  Write-Host ""
  Write-Host "[4/6] repair9 fix4 focused tests"
  python -m pytest -q `
    ".\phase159_r1_7c_r4_repair9_fix4_restore_and_safe_orphan_suppression\test_phase159_r1_7c_r4_repair9_fix4.py" `
    ".\tests\test_phase157_r20_repair30_final_reflexive_suppression.py"
  if ($LASTEXITCODE -ne 0) {
    throw "repair9 fix4 focused tests failed."
  }

  Write-Host ""
  Write-Host "[5/6] Current generic-route contract tests"
  python -m pytest -q `
    ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
    ".\tests\test_phase157_r20_repair12_map_property_reference_support.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Current generic-route contract tests failed."
  }

  Write-Host ""
  Write-Host "[6/6] Final targeted audit"
  python ".\phase159_r1_7c_r4_repair9_fix4_restore_and_safe_orphan_suppression\audit_phase159_r1_7c_r4_repair9_fix4.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Final targeted audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair9 fix4 focused verification completed."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
