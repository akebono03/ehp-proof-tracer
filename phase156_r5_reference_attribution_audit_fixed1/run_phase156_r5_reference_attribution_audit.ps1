$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R5 - Reference attribution audit (fixed1)"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/2] Focused classifier tests"
python -m pytest `
  ".\phase156_r5_reference_attribution_audit_fixed1\test_phase156_r5_attribution.py" `
  -q
Write-Host ""

Write-Host "[2/2] 112-group Reference attribution audit"
python -m `
  phase156_r5_reference_attribution_audit_fixed1.audit_phase156_r5_attribution `
  --output-dir ".\phase156_r5_attribution_audit_output"
Write-Host ""

Write-Host "Output:"
Write-Host "  .\phase156_r5_attribution_audit_output\phase156_r5_attribution_summary.txt"
Write-Host "  .\phase156_r5_attribution_audit_output\phase156_r5_attribution_suspicious.csv"
Write-Host "  .\phase156_r5_attribution_audit_output\phase156_r5_attribution_all_selected_statements.csv"
Write-Host ""
Write-Host "Repository-wide pytest is intentionally NOT run in this audit step."
