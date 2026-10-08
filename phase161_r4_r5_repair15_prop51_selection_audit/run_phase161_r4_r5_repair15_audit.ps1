$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=============================================================="
Write-Host "Phase 161-R4-R5 repair15 - Proposition 5.1 selection audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/2] Validate current files"
python -B -c "import ast, pathlib; files=['toda_group_proof_narrative_references.py','toda_group_proof_narrative_contribution_renderer.py','toda_literature_statement_boundary.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8'), filename=f) for f in files]; print('AST validation: PASS')"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Audit Proposition 5.1 selection"
python -B `
  ".\phase161_r4_r5_repair15_prop51_selection_audit\audit_phase161_r4_r5_repair15.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit completed."
Write-Host "Production changes: NONE"
Write-Host "Tests changed: NONE"
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
