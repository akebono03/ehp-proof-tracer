$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$OutputDir = Join-Path $RepoRoot "phase156_r5_repair2_output"

Write-Host "=============================================================="
Write-Host "Phase156-R5 repair2 — unused Reference header diagnostic"
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
    ".\phase156_r5_repair2_unused_header_diagnostic\test_phase156_r5_repair2_diagnostic.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 repair2 focused diagnostic tests failed."
  }

  Write-Host ""
  Write-Host "2/2 Reproduce and classify the four unused-header cases"
  python `
    ".\phase156_r5_repair2_unused_header_diagnostic\diagnose_phase156_r5_repair2.py" `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 repair2 diagnostic failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156-R5 repair2 diagnostic completed"
  Write-Host "=============================================================="
  Write-Host "Production changes: none"
  Write-Host ""
  Write-Host "Output:"
  Write-Host "  $OutputDir\phase156_r5_repair2_result.json"
  Write-Host "  $OutputDir\phase156_r5_repair2_full_cases.json"
  Write-Host ""
  Write-Host "Next boundary:"
  Write-Host "  decide whether header-without-marker is a real minimal-display defect"
  Write-Host "  or an allowed implicit-use rendering contract"
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}
