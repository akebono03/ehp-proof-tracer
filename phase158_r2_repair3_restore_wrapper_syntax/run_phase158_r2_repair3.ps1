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
Write-Host "Phase 158-R2 repair3 - restore baseline + syntax-safe wrapper"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/5] Restore exact pre-R2 renderer and apply wrapper"
python `
  ".\phase158_r2_repair3_restore_wrapper_syntax\apply_phase158_r2_repair3.py"
Assert-LastExitCode "apply repair3"

Write-Host "[2/5] Compile renderer"
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py"
Assert-LastExitCode "compile renderer"

Write-Host "[3/5] Focused tests"
python -m pytest `
  ".\phase158_r2_repair3_restore_wrapper_syntax\test_phase158_r2_repair3.py" `
  ".\tests\test_phase134_26_narrative_shell.py" `
  ".\tests\test_phase134_24_pi15_8_narrative.py" `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py" `
  ".\tests\test_phase154_r2_fix2_semantic_sentence_composition.py" `
  -q
Assert-LastExitCode "focused tests"

Write-Host "[4/5] 112-group contract + preservation audit"
python `
  ".\phase158_r2_repair3_restore_wrapper_syntax\audit_phase158_r2_repair3.py"
Assert-LastExitCode "112-group audit"

Write-Host "[5/5] Show summary"
Get-Content `
  ".\phase158_r2_repair3_restore_wrapper_syntax\output\phase158_r2_repair3_summary.txt" `
  -Encoding UTF8

Write-Host "=============================================================="
Write-Host "Phase 158-R2 repair3 complete."
Write-Host "Full repository pytest: NOT run"
Write-Host "=============================================================="
