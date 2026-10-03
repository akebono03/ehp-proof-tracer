$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R5 repair - (5.3) / Lemma 5.2 attribution separation"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/4] Apply minimal attribution repair"
python -m phase156_r5_reference_attribution_separation.apply_phase156_r5_repair
Write-Host ""

Write-Host "[2/4] Focused Phase156-R5 tests"
python -m pytest `
  ".\tests\test_phase156_r5_reference_attribution_separation.py" `
  -q
Write-Host ""

Write-Host "[3/4] Related existing tests"
python -m pytest `
  ".\tests\test_phase58_nu_prime_specialization.py" `
  ".\tests\test_phase58_lemma52_specialization.py" `
  ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py" `
  -q
Write-Host ""

Write-Host "[4/4] 112-group attribution reaudit"
python -m `
  phase156_r5_reference_attribution_separation.audit_phase156_r5_repair `
  --output-dir ".\phase156_r5_repair_audit_output"
Write-Host ""

Write-Host "Changed production file:"
Write-Host "  toda_rules.py"
Write-Host ""
Write-Host "Added test:"
Write-Host "  tests\test_phase156_r5_reference_attribution_separation.py"
Write-Host ""
Write-Host "Audit output:"
Write-Host "  phase156_r5_repair_audit_output\phase156_r5_repair_summary.txt"
Write-Host "  phase156_r5_repair_audit_output\phase156_r5_repair_suspicious.csv"
Write-Host ""
Write-Host "Repository-wide pytest is intentionally NOT run here."
