$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$ContributionTarget = Join-Path $RepoRoot "toda_group_proof_narrative_contribution_renderer.py"
$RendererTarget = Join-Path $RepoRoot "toda_group_proof_narrative_renderer.py"
$ContributionBackup = Join-Path $PackageRoot "backup_toda_group_proof_narrative_contribution_renderer.py"
$RendererBackup = Join-Path $PackageRoot "backup_toda_group_proof_narrative_renderer.py"
$OutputDir = Join-Path $RepoRoot "phase156_r4_audit_output"
$Applied = $false
$Succeeded = $false

Write-Host "=============================================================="
Write-Host "Phase156-R4 — proof-body duplicate suppression"
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
    -Path $ContributionTarget `
    -Destination $ContributionBackup `
    -Force

  Copy-Item `
    -Path $RendererTarget `
    -Destination $RendererBackup `
    -Force

  Write-Host "1/4 Apply Phase156-R4 production change"
  python `
    ".\phase156_r4_proof_body_duplicate_suppression_fixed1\apply_phase156_r4.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R4 production patch failed."
  }

  $Applied = $true

  Write-Host ""
  Write-Host "2/4 Focused suppression tests"
  python -m pytest `
    ".\phase156_r4_proof_body_duplicate_suppression_fixed1\test_phase156_r4_body_restatement_suppression.py" `
    ".\tests\test_phase154_r2_fix3_reference_marker_completion.py" `
    ".\tests\test_phase153_r8_reference_use_prose_normalization.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R4 focused suppression tests failed."
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
    throw "Phase156-R4 public Reference audit-only regression failed."
  }

  Write-Host ""
  Write-Host "4/4 112-group body-restatement audit"
  python `
    ".\phase156_r4_proof_body_duplicate_suppression_fixed1\audit_phase156_r4.py" `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R4 112-group audit failed."
  }

  $Succeeded = $true

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156-R4 completed"
  Write-Host "=============================================================="
  Write-Host "Production files changed:"
  Write-Host "  toda_group_proof_narrative_contribution_renderer.py"
  Write-Host "  toda_group_proof_narrative_renderer.py"
  Write-Host ""
  Write-Host "Output:"
  Write-Host "  $OutputDir\phase156_r4_summary.txt"
  Write-Host "  $OutputDir\phase156_r4_result.json"
  Write-Host "  $OutputDir\phase156_r4_preserved_derivational.json"
  Write-Host ""
  Write-Host "Repository-wide pytest: NOT run"
  Write-Host "Next boundary:"
  Write-Host "  Phase156-R5 — 112-group cross-group Reference minimal-display audit"
}
finally {
  if ($Applied -and -not $Succeeded) {
    Write-Host ""
    Write-Host "Phase156-R4 failed; restoring production files from backup."

    Copy-Item `
      -Path $ContributionBackup `
      -Destination $ContributionTarget `
      -Force

    Copy-Item `
      -Path $RendererBackup `
      -Destination $RendererTarget `
      -Force
  }

  $env:PYTHONPATH = $OriginalPythonPath
}
