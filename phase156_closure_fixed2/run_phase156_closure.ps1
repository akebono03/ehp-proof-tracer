$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$BackupRoot = Join-Path $PackageRoot "backup_documents"

$Documents = @(
  "README.md",
  "docs\design.md",
  "docs\development_log.md",
  "docs\roadmap.md",
  "docs\proof_records.md"
)

$ExpectedHead = "baab9402c9ca8c5051268d5d334591ea44b5b273"
$Applied = $false
$Succeeded = $false

Write-Host "=============================================================="
Write-Host "Phase156 closure — documentation + repository-wide pytest"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
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
  $CurrentHead = (git rev-parse HEAD).Trim()

  Write-Host "Current git HEAD:"
  Write-Host $CurrentHead
  Write-Host ""

  if ($CurrentHead -ne $ExpectedHead) {
    throw "Phase156 closure expected HEAD $ExpectedHead but found $CurrentHead."
  }

  if (Test-Path $BackupRoot) {
    Remove-Item `
      -Path $BackupRoot `
      -Recurse `
      -Force
  }

  New-Item `
    -ItemType Directory `
    -Path $BackupRoot `
    -Force `
    | Out-Null

  foreach ($RelativePath in $Documents) {
    $Source = Join-Path $RepoRoot $RelativePath
    $Backup = Join-Path $BackupRoot $RelativePath
    $BackupParent = Split-Path -Parent $Backup

    New-Item `
      -ItemType Directory `
      -Path $BackupParent `
      -Force `
      | Out-Null

    Copy-Item `
      -Path $Source `
      -Destination $Backup `
      -Force
  }

  Write-Host "1/4 Build and apply full Phase156 closure documents"
  python `
    ".\phase156_closure\build_phase156_closure_documents.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156 closure document generation failed."
  }

  $Applied = $true

  Write-Host ""
  Write-Host "2/4 Validate closure documents"
  python `
    ".\phase156_closure\validate_phase156_closure_documents.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156 closure document validation failed."
  }

  Write-Host ""
  Write-Host "3/4 Repository-wide pytest"
  python -m pytest

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156 repository-wide pytest failed."
  }

  Write-Host ""
  Write-Host "4/4 Audit-only exact-node regression"

  python -m pytest `
    --noconftest `
    "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_group_reference_population_invariants" `
    "tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api" `
    -q `
    --tb=short `
    -p no:cacheprovider `
    -o addopts=

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156 audit-only exact-node regression failed."
  }

  $Succeeded = $true

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156 closure completed"
  Write-Host "=============================================================="
  Write-Host "Production code changes: none"
  Write-Host ""
  Write-Host "Updated full documents:"
  Write-Host "  README.md"
  Write-Host "  docs\design.md"
  Write-Host "  docs\development_log.md"
  Write-Host "  docs\roadmap.md"
  Write-Host "  docs\proof_records.md"
  Write-Host ""
  Write-Host "Full generated copies:"
  Write-Host "  phase156_closure_output\documents\README.md"
  Write-Host "  phase156_closure_output\documents\docs\design.md"
  Write-Host "  phase156_closure_output\documents\docs\development_log.md"
  Write-Host "  phase156_closure_output\documents\docs\roadmap.md"
  Write-Host "  phase156_closure_output\documents\docs\proof_records.md"
  Write-Host ""
  Write-Host "Next boundary:"
  Write-Host "  If all tests passed, Phase156 is complete."
  Write-Host "  Phase157 planning starts only after this closure result."
}
finally {
  if ($Applied -and -not $Succeeded) {
    Write-Host ""
    Write-Host "Phase156 closure failed; restoring the five documents."

    foreach ($RelativePath in $Documents) {
      $Backup = Join-Path $BackupRoot $RelativePath
      $Target = Join-Path $RepoRoot $RelativePath

      if (Test-Path $Backup) {
        Copy-Item `
          -Path $Backup `
          -Destination $Target `
          -Force
      }
    }
  }

  $env:PYTHONPATH = $OriginalPythonPath
}
