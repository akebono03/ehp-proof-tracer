$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupRoot = Join-Path `
  (Split-Path -Parent $RepoRoot) `
  ("ehp_proof_phase155_r2c_backup_" + $Timestamp)

Write-Host "=============================================================="
Write-Host "Phase 155-R2C - confirmed stale expectation repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing-test changes: confirmed-stale functions only"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

Write-Host "1/4 Focused tests for the R2C repair tool only"
python -m pytest `
  "$PackageDir\test_repair_phase155_r2c.py" `
  -q `
  -p no:cacheprovider
if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R2C repair-tool tests failed."
}

Write-Host ""
Write-Host "2/4 Backup changed test files outside the repository"
New-Item `
  -ItemType Directory `
  -Path $BackupRoot `
  -Force | Out-Null

$NodeIds = Get-Content `
  "$PackageDir\confirmed_stale_nodeids.txt"

$Files = $NodeIds |
  ForEach-Object {
    ($_ -split "::")[0]
  } |
  Sort-Object -Unique

foreach ($RelativeFile in $Files) {
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
Write-Host "3/4 Apply only confirmed-stale expectation repairs"
python `
  "$PackageDir\repair_phase155_r2c.py" `
  --repo-root "$RepoRoot"
if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R2C repair application failed."
}

Write-Host ""
Write-Host "4/4 Re-run the R2B focused verification set"
$R2BTool = Join-Path `
  $RepoRoot `
  "phase155_r2b_stale_candidate_verification\audit_phase155_r2b.py"

if (-not (Test-Path $R2BTool)) {
  throw "R2B verification tool not found: $R2BTool"
}

python `
  "$R2BTool" `
  --repo-root "$RepoRoot" `
  --output-dir "phase155_r2c_verification_output"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R2C focused verification did not complete."
}

$MetadataPath = Join-Path `
  $RepoRoot `
  "phase155_r2c_verification_output\phase155_r2b_metadata.json"

$Metadata = Get-Content `
  $MetadataPath `
  -Raw |
  ConvertFrom-Json

$ConfirmedStale = 0
if (
  $null -ne
  $Metadata.verification_class_counts.confirmed_stale
) {
  $ConfirmedStale = [int](
    $Metadata.verification_class_counts.confirmed_stale
  )
}

$Inconclusive = 0
if (
  $null -ne
  $Metadata.verification_class_counts.verification_inconclusive
) {
  $Inconclusive = [int](
    $Metadata.verification_class_counts.verification_inconclusive
  )
}

if ($Metadata.pytest_exit_code -ne 0) {
  throw (
    "R2C focused verification still has failing tests. "
    + "pytest exit code: "
    + $Metadata.pytest_exit_code
  )
}

if ($ConfirmedStale -ne 0) {
  throw (
    "R2C focused verification still has confirmed stale findings: "
    + $ConfirmedStale
  )
}

if ($Inconclusive -ne 0) {
  throw (
    "R2C focused verification has inconclusive findings: "
    + $Inconclusive
  )
}

Write-Host ""
Write-Host "Phase 155-R2C completed."
Write-Host "confirmed stale after repair: $ConfirmedStale"
Write-Host "inconclusive after repair: $Inconclusive"
Write-Host "repository-wide pytest: NOT run"
Write-Host "Backup: $BackupRoot"
Write-Host (
  "Summary: "
  + $RepoRoot
  + "\phase155_r2c_verification_output\phase155_r2b_summary.md"
)
