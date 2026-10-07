$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159-R1-7 - cross-group display audit"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PhaseDir = Join-Path $RepoRoot "phase159_r1_7_cross_group_audit"
$AuditScript = Join-Path $PhaseDir "audit_phase159_r1_7.py"
$OutputDir = Join-Path $PhaseDir "audit_output"

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host "Production code changes: none"
  Write-Host "Existing test changes: none"
  Write-Host ""

  Write-Host "[1/3] Syntax preflight"
  python -m py_compile $AuditScript

  if ($LASTEXITCODE -ne 0) {
    throw "Phase 159-R1-7 syntax preflight failed."
  }

  Write-Host ""
  Write-Host "[2/3] Run four-group public Narrative audit"

  if (Test-Path $OutputDir) {
    Remove-Item $OutputDir -Recurse -Force
  }

  python $AuditScript

  if ($LASTEXITCODE -ne 0) {
    throw "Phase 159-R1-7 audit failed."
  }

  Write-Host ""
  Write-Host "[3/3] Show generated files"
  Get-ChildItem $OutputDir | Select-Object Name, Length

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 159-R1-7 audit completed."
  Write-Host "No production files were changed."
  Write-Host "No repository tests were added or changed."
  Write-Host "Full pytest was intentionally not run."
  Write-Host "Review:"
  Write-Host "  $OutputDir\phase159_r1_7_summary.md"
  Write-Host "  $OutputDir\phase159_r1_7_audit.json"
  Write-Host "  $OutputDir\pi6_3.md"
  Write-Host "  $OutputDir\pi8_5.md"
  Write-Host "  $OutputDir\pi10_4.md"
  Write-Host "  $OutputDir\pi11_4.md"
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
