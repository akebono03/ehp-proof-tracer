$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146 Final Regression Documentation Append"
Write-Host "Minimal diff: final repository-wide result only"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$Targets = @(
  "docs/development_log.md",
  "docs/proof_records.md"
)

Write-Host "`nA. Verifying documentation starts clean..."
$Before = git diff --name-only -- $Targets
if ($Before) {
  Write-Host "ERROR: target documentation already has local changes:"
  Write-Host $Before
  exit 2
}
Write-Host "Target documentation clean: PASS"

Write-Host "`nB. Applying minimal final-regression append..."
python "$PackageDir\apply_phase146_final_regression_documentation_append.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Diff verification..."
git diff --check -- $Targets
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git diff --numstat -- $Targets
git diff -- $Targets

Write-Host "`nD. Verifying exact final result..."
python -c "from pathlib import Path; files=['docs/development_log.md','docs/proof_records.md']; result='10306 passed in 1304.31s (0:21:44)'; assert all(Path(p).read_text(encoding='utf-8').count(result)==1 for p in files); print('Final regression marker: PASS')"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n=============================================================="
Write-Host "Completion criteria:"
Write-Host "  - development_log.md: final result appended once"
Write-Host "  - proof_records.md: final result appended once"
Write-Host "  - minimal diff only"
Write-Host "  - production changes: none"
Write-Host "  - test changes: none"
Write-Host "  - README/design/roadmap unchanged"
Write-Host "  - no pytest rerun; result records the just-completed whole suite"
Write-Host "=============================================================="
