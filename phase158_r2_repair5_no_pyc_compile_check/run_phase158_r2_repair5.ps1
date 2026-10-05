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
Write-Host "Phase 158-R2 repair5 - no-pyc syntax check"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/4] Syntax check without writing __pycache__"
python -c "from pathlib import Path; p=Path('toda_group_proof_narrative_renderer.py'); compile(p.read_text(encoding='utf-8'), str(p), 'exec'); print('Syntax check: PASS')"
Assert-LastExitCode "syntax check"

Write-Host "[2/4] Focused Phase 158 baseline-preservation tests"
python -m pytest `
  ".\phase158_r2_repair4_baseline_preserving_normalization\test_phase158_r2_repair4.py" `
  ".\tests\test_phase134_26_narrative_shell.py" `
  ".\tests\test_phase153_r10_used_reference_filtering.py" `
  ".\tests\test_phase154_r5_fix1_graph_backed_reference_linkage.py" `
  -q
Assert-LastExitCode "focused tests"

Write-Host "[3/4] 112-group baseline-preservation audit"
python `
  ".\phase158_r2_repair4_baseline_preserving_normalization\audit_phase158_r2_repair4.py"
Assert-LastExitCode "112-group preservation audit"

Write-Host "[4/4] Show summary"
Get-Content `
  ".\phase158_r2_repair4_baseline_preserving_normalization\output\phase158_r2_repair4_summary.txt" `
  -Encoding UTF8

Write-Host "=============================================================="
Write-Host "Phase 158-R2 repair5 complete."
Write-Host "Production code changes: none"
Write-Host "Full repository pytest: NOT run"
Write-Host "=============================================================="
