$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146 Documentation Clean-Diff Repair R2"
Write-Host "Encoding-safe verification only"
Write-Host "Documentation changes: none"
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

Write-Host "`nA. Verifying documentation diff remains clean..."
$DocDiff = git diff --name-only -- $Targets
if ($DocDiff) {
  Write-Host "ERROR: documentation diff is not clean:"
  Write-Host $DocDiff
  git diff --numstat -- $Targets
  git diff --check -- $Targets
  exit 2
}
Write-Host "Documentation clean diff: PASS"

Write-Host "`nB. Encoding-safe Phase 146 marker verification..."
python "$PackageDir\verify_phase146_documentation_clean_diff_r2.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Confirming documentation remains unchanged..."
$DocDiffAfter = git diff --name-only -- $Targets
if ($DocDiffAfter) {
  Write-Host "ERROR: verification unexpectedly changed documentation:"
  Write-Host $DocDiffAfter
  exit 3
}
Write-Host "Documentation unchanged by R2: PASS"

Write-Host "`nD. Repository tracked diff summary..."
git diff --stat
git status --short

Write-Host "`n=============================================================="
Write-Host "R2 completion criteria:"
Write-Host "  - documentation diff is empty"
Write-Host "  - UTF-8 strict decode passes for all four documents"
Write-Host "  - Phase 146 markers pass through Python UTF-8 verification"
Write-Host "  - documentation changes: none"
Write-Host "  - production changes: none"
Write-Host "  - test changes: none"
Write-Host "  - no pytest is run"
Write-Host "=============================================================="
