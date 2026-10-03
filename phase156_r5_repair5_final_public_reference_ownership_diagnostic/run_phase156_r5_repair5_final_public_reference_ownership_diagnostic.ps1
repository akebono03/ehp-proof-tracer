$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$OutputDir = Join-Path $RepoRoot "phase156_r5_repair5_output"

Write-Host "=============================================================="
Write-Host "Phase156-R5 repair5 — final public Reference ownership diagnostic"
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

  Write-Host "1/2 Focused diagnostic tests"
  python -m pytest `
    ".\phase156_r5_repair5_final_public_reference_ownership_diagnostic\test_phase156_r5_repair5_diagnostic.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 repair5 focused diagnostic tests failed."
  }

  Write-Host ""
  Write-Host "2/2 Map final public Reference headers to graph entries"
  python `
    ".\phase156_r5_repair5_final_public_reference_ownership_diagnostic\diagnose_phase156_r5_repair5.py" `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 repair5 ownership diagnostic failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156-R5 repair5 diagnostic completed"
  Write-Host "=============================================================="
  Write-Host "Production changes: none"
  Write-Host ""
  Write-Host "Output:"
  Write-Host "  $OutputDir\phase156_r5_repair5_result.json"
  Write-Host ""
  Write-Host "Next boundary:"
  Write-Host "  classify final public statements as Reference-owned,"
  Write-Host "  proof-body-owned, or mixed before production repair"
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}
