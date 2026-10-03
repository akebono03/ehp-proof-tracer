$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$OutputDir = Join-Path $RepoRoot "phase156_r2_audit_output"

Write-Host "=============================================================="
Write-Host "Phase156-R2 — consumer usage relevance audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

Set-Location $RepoRoot

$OriginalPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($OriginalPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = $RepoRoot + [IO.Path]::PathSeparator + $OriginalPythonPath
}

try {
  Write-Host "Current git HEAD:"
  git rev-parse HEAD
  Write-Host ""

  Write-Host "1/2 Focused consumer-classifier tests"
  python -m pytest `
    ".\phase156_r2_consumer_usage_relevance_audit\test_phase156_r2_audit_classifier.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R2 focused classifier tests failed."
  }

  Write-Host ""
  Write-Host "2/2 112-group / 103-overfull consumer-usage audit"
  python `
    ".\phase156_r2_consumer_usage_relevance_audit\audit_phase156_r2.py" `
    --repo-root "$RepoRoot" `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R2 audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156-R2 completed"
  Write-Host "=============================================================="
  Write-Host "Output:"
  Write-Host "  $OutputDir\phase156_r2_summary.txt"
  Write-Host "  $OutputDir\phase156_r2_consumer_usage_classification.csv"
  Write-Host "  $OutputDir\phase156_r2_classification_summary.csv"
  Write-Host "  $OutputDir\phase156_r2_result.json"
  Write-Host ""
  Write-Host "Next boundary:"
  Write-Host "  Phase156-R3 — minimal Reference statement selection rule"
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}
