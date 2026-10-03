$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$OutputDir = Join-Path $RepoRoot "phase156_r5_audit_output"

Write-Host "=============================================================="
Write-Host "Phase156-R5 — 112-group cross-group Reference minimal-display audit"
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

  Write-Host "1/4 Focused audit-classifier tests"
  python -m pytest `
    ".\phase156_r5_cross_group_reference_minimal_display_audit_fixed1\test_phase156_r5_audit_classifier.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 focused audit-classifier tests failed."
  }

  Write-Host ""
  Write-Host "2/4 Phase153 public Reference audit-only regression"
  python -m pytest `
    --noconftest `
    "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_group_reference_population_invariants" `
    -q `
    --tb=short `
    -p no:cacheprovider `
    -o addopts=

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 Phase153 audit-only regression failed."
  }

  Write-Host ""
  Write-Host "3/4 Phase155 audit-boundary contract"
  python -m pytest `
    ".\tests\test_phase155_audit_boundary.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 Phase155 audit-boundary contract failed."
  }

  Write-Host ""
  Write-Host "4/4 112-group cross-group Reference minimal-display audit"
  python `
    ".\phase156_r5_cross_group_reference_minimal_display_audit_fixed1\audit_phase156_r5.py" `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 112-group cross-group audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156-R5 completed"
  Write-Host "=============================================================="
  Write-Host "Production changes: none"
  Write-Host ""
  Write-Host "Output:"
  Write-Host "  $OutputDir\phase156_r5_summary.txt"
  Write-Host "  $OutputDir\phase156_r5_result.json"
  Write-Host "  $OutputDir\phase156_r5_group_summary.csv"
  Write-Host "  $OutputDir\phase156_r5_violations.csv"
  Write-Host "  $OutputDir\phase156_r5_violation_summary.csv"
  Write-Host ""
  Write-Host "Repository-wide pytest: NOT run"
  Write-Host "Next boundary:"
  Write-Host "  Phase156-R6 — focused/sharded regression"
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}
