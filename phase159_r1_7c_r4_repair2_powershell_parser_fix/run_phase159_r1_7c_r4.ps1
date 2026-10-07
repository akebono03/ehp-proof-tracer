$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 repair2 - PowerShell/PYTHONPATH fix"
Write-Host "=============================================================="

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

$OriginalPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($OriginalPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = $RepoRoot + [IO.Path]::PathSeparator + $OriginalPythonPath
}

try {
  Write-Host "[1/2] Run R4 audit"

  python ".\phase159_r1_7c_r4_cross_group_structural_audit\audit_phase159_r1_7c_r4.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase 159 R1-7c R4 audit failed with exit code $LASTEXITCODE."
  }

  $SummaryPath = ".\phase159_r1_7c_r4_cross_group_structural_audit\output\summary.md"

  if (-not (Test-Path $SummaryPath)) {
    throw "Phase 159 R1-7c R4 audit completed without creating output\summary.md."
  }

  Write-Host ""
  Write-Host "[2/2] Show summary"

  Get-Content $SummaryPath -Encoding UTF8

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R4 audit complete"
  Write-Host "Production code changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide pytest: not run"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}
