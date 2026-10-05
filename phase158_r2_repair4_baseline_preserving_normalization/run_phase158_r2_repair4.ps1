$ErrorActionPreference = "Stop"

function Assert-LastExitCode {
  param(
    [string]$Step
  )

  if ($LASTEXITCODE -ne 0) {
    throw "$Step failed with exit code $LASTEXITCODE"
  }
}

Write-Host "=============================================================="
Write-Host "Phase 158-R2 repair4 - baseline-preserving normalization"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/5] Restore exact pre-R2 renderer and apply wrapper"
python `
  ".\phase158_r2_repair4_baseline_preserving_normalization\apply_phase158_r2_repair4.py"
Assert-LastExitCode "apply repair4"

Write-Host "[2/5] Compile renderer"
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py"
Assert-LastExitCode "compile renderer"

Write-Host "[3/5] Focused Phase 158 baseline-preservation tests"
python -m pytest `
  ".\phase158_r2_repair4_baseline_preserving_normalization\test_phase158_r2_repair4.py" `
  ".\tests\test_phase134_26_narrative_shell.py" `
  ".\tests\test_phase153_r10_used_reference_filtering.py" `
  ".\tests\test_phase154_r5_fix1_graph_backed_reference_linkage.py" `
  -q
Assert-LastExitCode "focused tests"

Write-Host "[4/5] 112-group baseline-preservation audit"
python `
  ".\phase158_r2_repair4_baseline_preserving_normalization\audit_phase158_r2_repair4.py"
Assert-LastExitCode "112-group preservation audit"

Write-Host "[5/5] Show summary"
Get-Content `
  ".\phase158_r2_repair4_baseline_preserving_normalization\output\phase158_r2_repair4_summary.txt" `
  -Encoding UTF8

Write-Host "=============================================================="
Write-Host "Phase 158-R2 repair4 complete."
Write-Host "Full repository pytest: NOT run"
Write-Host "=============================================================="
