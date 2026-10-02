$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupRoot = Join-Path `
  (Split-Path -Parent $RepoRoot) `
  ("ehp_proof_phase155_r2c_r2_backup_" + $Timestamp)

Write-Host "=============================================================="
Write-Host "Phase 155-R2C-r2 - remaining stale expectation repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: 2 test functions only"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

Write-Host "1/4 Focused tests for the R2C-r2 repair tool only"

python -m pytest `
  "$PackageDir\test_repair_phase155_r2c_r2.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R2C-r2 repair-tool tests failed."
}

Write-Host ""
Write-Host "2/4 Backup the two changed test files outside the repository"

New-Item `
  -ItemType Directory `
  -Path $BackupRoot `
  -Force | Out-Null

$TargetFiles = @(
  "tests\test_phase132_6_group_proof_narrative_renderer.py",
  "tests\test_phase153_r12_root_reference_exclusion.py"
)

foreach ($RelativeFile in $TargetFiles) {
  $Source = Join-Path $RepoRoot $RelativeFile
  $Destination = Join-Path $BackupRoot $RelativeFile
  $DestinationDir = Split-Path -Parent $Destination

  New-Item `
    -ItemType Directory `
    -Path $DestinationDir `
    -Force | Out-Null

  Copy-Item `
    -Path $Source `
    -Destination $Destination `
    -Force
}

Write-Host "Backup: $BackupRoot"

Write-Host ""
Write-Host "3/4 Apply the two remaining expectation repairs"

python `
  "$PackageDir\repair_phase155_r2c_r2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R2C-r2 repair application failed."
}

Write-Host ""
Write-Host "Focused check of the two previously failing tests"

python -m pytest `
  "tests/test_phase132_6_group_proof_narrative_renderer.py::test_phase132_6_sigma9_narrative_uses_fixed_japanese_leads" `
  "tests/test_phase153_r12_root_reference_exclusion.py::test_phase153_r12_pi11_4_body_uses_renumbered_external_references" `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "The two R2C-r2 focused tests still fail."
}

Write-Host ""
Write-Host "4/4 Re-run the complete R2B focused verification set"

$R2BTool = Join-Path `
  $RepoRoot `
  "phase155_r2b_stale_candidate_verification\audit_phase155_r2b.py"

if (-not (Test-Path $R2BTool)) {
  throw "R2B verification tool not found: $R2BTool"
}

python `
  "$R2BTool" `
  --repo-root "$RepoRoot" `
  --output-dir "phase155_r2c_r2_verification_output"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R2C-r2 verification audit did not complete."
}

$MetadataPath = Join-Path `
  $RepoRoot `
  "phase155_r2c_r2_verification_output\phase155_r2b_metadata.json"

$Metadata = Get-Content `
  $MetadataPath `
  -Raw |
  ConvertFrom-Json

$ConfirmedStale = 0
if ($null -ne $Metadata.verification_class_counts.confirmed_stale) {
  $ConfirmedStale = [int]$Metadata.verification_class_counts.confirmed_stale
}

$Inconclusive = 0
if ($null -ne $Metadata.verification_class_counts.verification_inconclusive) {
  $Inconclusive = [int]$Metadata.verification_class_counts.verification_inconclusive
}

if ($Metadata.pytest_exit_code -ne 0) {
  throw "R2C-r2 focused verification still has failing tests. pytest exit code: $($Metadata.pytest_exit_code)"
}

if ($ConfirmedStale -ne 0) {
  throw "R2C-r2 focused verification still has confirmed stale findings: $ConfirmedStale"
}

if ($Inconclusive -ne 0) {
  throw "R2C-r2 focused verification has inconclusive findings: $Inconclusive"
}

Write-Host ""
Write-Host "Phase 155-R2C-r2 completed."
Write-Host "confirmed stale after repair: $ConfirmedStale"
Write-Host "inconclusive after repair: $Inconclusive"
Write-Host "repository-wide pytest: NOT run"
Write-Host "Backup: $BackupRoot"
Write-Host "Summary: $RepoRoot\phase155_r2c_r2_verification_output\phase155_r2b_summary.md"
