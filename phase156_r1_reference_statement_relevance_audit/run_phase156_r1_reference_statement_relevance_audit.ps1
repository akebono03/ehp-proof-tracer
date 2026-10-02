$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$OutputDir = Join-Path $RepoRoot "phase156_r1_audit_output"

Write-Host "=============================================================="
Write-Host "Phase156-R1 — Reference statement relevance / minimal display"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

Set-Location $RepoRoot

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "1/2 Focused classifier tests"
python -m pytest `
  ".\phase156_r1_reference_statement_relevance_audit\test_phase156_r1_audit_classifier.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase156-R1 focused classifier tests failed."
}

Write-Host ""
Write-Host "2/2 112-group / 117-duplicate classification audit"
python `
  ".\phase156_r1_reference_statement_relevance_audit\audit_phase156_r1.py" `
  --repo-root "$RepoRoot" `
  --output-dir "$OutputDir"

if ($LASTEXITCODE -ne 0) {
  throw "Phase156-R1 audit failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase156-R1 completed"
Write-Host "=============================================================="
Write-Host "Output:"
Write-Host "  $OutputDir\phase156_r1_summary.txt"
Write-Host "  $OutputDir\phase156_r1_duplicate_classification.csv"
Write-Host "  $OutputDir\phase156_r1_classification_summary.csv"
Write-Host "  $OutputDir\phase156_r1_result.json"
Write-Host ""
Write-Host "Next boundary:"
Write-Host "  Phase156-R2 — consumer usage based relevance rule design"
