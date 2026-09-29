$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146 Documentation Clean-Diff Repair"
Write-Host "Remove documentation newline/diff noise only"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$Targets = @(
  "docs/design.md",
  "docs/development_log.md",
  "docs/roadmap.md",
  "docs/proof_records.md"
)

Write-Host "`nA. Current documentation diff before repair..."
git diff --numstat -- $Targets
git diff --stat -- $Targets

Write-Host "`nB. Verifying HEAD Phase 146 markers and restoring canonical bytes..."
python "$PackageDir\apply_phase146_documentation_clean_diff_repair.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Documentation diff after repair..."
$DocDiff = git diff --name-only -- $Targets
if ($DocDiff) {
  Write-Host "ERROR: documentation diff remains after canonical restore:"
  Write-Host $DocDiff
  git diff --numstat -- $Targets
  git diff --check -- $Targets
  exit 3
}
Write-Host "Documentation clean diff: PASS"

Write-Host "`nD. Repository diff summary after documentation cleanup..."
git diff --stat
git status --short

Write-Host "`nE. Phase 146 documentation marker verification..."
$Checks = @(
  @("docs/design.md", "Phase 146 closure boundary"),
  @("docs/development_log.md", "Phase 146 完了境界"),
  @("docs/roadmap.md", "Phase 147 — RC1"),
  @("docs/roadmap.md", "Phase 152 — RC6"),
  @("docs/proof_records.md", "Phase 146 historical Narrative comparison / provenance record")
)

foreach ($Check in $Checks) {
  $File = $Check[0]
  $Marker = $Check[1]
  $Found = Select-String -Path $File -SimpleMatch $Marker -Quiet
  if (-not $Found) {
    Write-Host "ERROR: missing marker '$Marker' in $File"
    exit 4
  }
}
Write-Host "Phase 146 documentation markers: PASS"

Write-Host "`n=============================================================="
Write-Host "Documentation Clean-Diff Repair completion criteria:"
Write-Host "  - canonical HEAD contains Phase 146 closure markers"
Write-Host "  - four documentation files restored byte-for-byte from HEAD"
Write-Host "  - documentation diff is empty"
Write-Host "  - UTF-8 strict decode passes"
Write-Host "  - production changes: none"
Write-Host "  - test changes: none"
Write-Host "  - README.md unchanged"
Write-Host "  - no pytest is run because this repair changes documentation only"
Write-Host ""
Write-Host "The final Phase 146 repository-wide regression result is intentionally"
Write-Host "not appended here. Run the whole suite once after Repairs 1-9, then"
Write-Host "record that final post-performance result in the closure documents."
Write-Host "=============================================================="
