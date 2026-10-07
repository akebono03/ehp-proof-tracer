$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 numbered pipeline audit"
Write-Host "No production changes"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PreviousPythonPath = $env:PYTHONPATH
$PathSeparator = [System.IO.Path]::PathSeparator

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = [string]::Concat(
    $RepoRoot,
    $PathSeparator,
    $PreviousPythonPath
  )
}

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  python ".\phase159_pi3_2_numbered_pipeline_audit\audit_phase159_pi3_2_numbered_pipeline.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Audit complete"
  Write-Host "Production changes: NONE"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
