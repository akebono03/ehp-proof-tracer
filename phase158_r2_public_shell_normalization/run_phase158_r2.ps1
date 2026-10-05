$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R2 - Narrative Public Shell Normalization"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/4] Apply Phase 158-R2"
python `
  ".\phase158_r2_public_shell_normalization\apply_phase158_r2.py"

Write-Host "[2/4] Focused Phase 158-R2 tests"
python -m pytest `
  ".\phase158_r2_public_shell_normalization\test_phase158_r2_public_shell_normalization.py" `
  ".\tests\test_phase134_26_narrative_shell.py" `
  ".\tests\test_phase134_24_pi15_8_narrative.py" `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py" `
  -q

Write-Host "[3/4] 112-group contract audit"
python `
  ".\phase158_r2_public_shell_normalization\audit_phase158_r2.py"

Write-Host "[4/4] Show summary"
Get-Content `
  ".\phase158_r2_public_shell_normalization\output\phase158_r2_summary.txt" `
  -Encoding UTF8

Write-Host "=============================================================="
Write-Host "Phase 158-R2 complete."
Write-Host "Full repository pytest: NOT run"
Write-Host "=============================================================="
