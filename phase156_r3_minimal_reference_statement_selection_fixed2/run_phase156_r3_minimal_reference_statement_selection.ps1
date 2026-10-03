$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$Target = Join-Path $RepoRoot "toda_group_proof_narrative_references.py"
$Backup = Join-Path $PackageRoot "backup_toda_group_proof_narrative_references.py"
$OutputDir = Join-Path $RepoRoot "phase156_r3_audit_output"
$Applied = $false
$Succeeded = $false

Write-Host "=============================================================="
Write-Host "Phase156-R3 — minimal Reference statement selection rule"
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

  Write-Host "1/4 Apply production change"
  python `
    ".\phase156_r3_minimal_reference_statement_selection_fixed2\apply_phase156_r3.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R3 production patch failed."
  }
  $Applied = $true

  Write-Host ""
  Write-Host "2/4 Focused selector regression tests"
  python -m pytest `
    ".\tests\test_phase153_r3_3_reference_statement_selection.py" `
    ".\tests\test_phase153_r5_reference_selection.py" `
    ".\tests\test_phase153_r6_reference_granularity.py" `
    ".\phase156_r3_minimal_reference_statement_selection_fixed2\test_phase156_r3_minimal_reference_selection.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R3 focused selector regression tests failed."
  }

  Write-Host ""
  Write-Host "3/4 Public Reference connection audit-only regression"
  python -m pytest `
    --noconftest `
    "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_group_reference_population_invariants" `
    -q `
    --tb=short `
    -p no:cacheprovider `
    -o addopts=

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R3 public Reference audit-only regression failed."
  }

  Write-Host ""
  Write-Host "4/4 112-group minimal-selection audit"
  python `
    ".\phase156_r3_minimal_reference_statement_selection_fixed2\audit_phase156_r3.py" `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R3 112-group audit failed."
  }

  $Succeeded = $true

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156-R3 completed"
  Write-Host "=============================================================="
  Write-Host "Production file changed:"
  Write-Host "  toda_group_proof_narrative_references.py"
  Write-Host ""
  Write-Host "Output:"
  Write-Host "  $OutputDir\phase156_r3_summary.txt"
  Write-Host "  $OutputDir\phase156_r3_result.json"
  Write-Host ""
  Write-Host "Repository-wide pytest: NOT run"
  Write-Host "Next boundary:"
  Write-Host "  Phase156-R4 — proof-body duplicate suppression"
}
finally {
  if ($Applied -and -not $Succeeded) {
    Write-Host ""
    Write-Host "Phase156-R3 failed; restoring production file from backup."
    Copy-Item `
      -Path $Backup `
      -Destination $Target `
      -Force
  }

  $env:PYTHONPATH = $OriginalPythonPath
}
