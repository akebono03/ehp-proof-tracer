$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$Target = Join-Path $RepoRoot "toda_group_proof_narrative_contribution_renderer.py"
$Backup = Join-Path $PackageRoot "backup_toda_group_proof_narrative_contribution_renderer.py"
$OutputDir = Join-Path $RepoRoot "phase156_r5_repair3_audit_output"
$Applied = $false
$Succeeded = $false

Write-Host "=============================================================="
Write-Host "Phase156-R5 repair3 — generic final Reference suppression"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
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

  Copy-Item `
    -Path $Target `
    -Destination $Backup `
    -Force

  Write-Host "1/4 Apply production repair"
  python `
    ".\phase156_r5_repair3_generic_final_suppression\apply_phase156_r5_repair3.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 repair3 production patch failed."
  }

  $Applied = $true

  Write-Host ""
  Write-Host "2/4 Focused generic-route regression"
  python -m pytest `
    ".\phase156_r5_repair3_generic_final_suppression\test_phase156_r5_repair3_generic_suppression.py" `
    ".\tests\test_phase154_r2_fix3_reference_marker_completion.py" `
    ".\tests\test_phase153_r8_reference_use_prose_normalization.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 repair3 focused regression failed."
  }

  Write-Host ""
  Write-Host "3/4 Public Reference audit-only regression"
  python -m pytest `
    --noconftest `
    "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_group_reference_population_invariants" `
    -q `
    --tb=short `
    -p no:cacheprovider `
    -o addopts=

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 repair3 public Reference regression failed."
  }

  Write-Host ""
  Write-Host "4/4 112-group repaired R5 audit"
  python `
    ".\phase156_r5_repair3_generic_final_suppression\audit_phase156_r5_repair3.py" `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R5 repair3 112-group audit failed."
  }

  $Succeeded = $true

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156-R5 repair3 completed"
  Write-Host "=============================================================="
  Write-Host "Production file changed:"
  Write-Host "  toda_group_proof_narrative_contribution_renderer.py"
  Write-Host ""
  Write-Host "Repository-wide pytest: NOT run"
  Write-Host "Next boundary:"
  Write-Host "  Phase156-R6 — focused/sharded regression"
}
finally {
  if ($Applied -and -not $Succeeded) {
    Write-Host ""
    Write-Host "Phase156-R5 repair3 failed; restoring production file from backup."

    Copy-Item `
      -Path $Backup `
      -Destination $Target `
      -Force
  }

  $env:PYTHONPATH = $OriginalPythonPath
}
