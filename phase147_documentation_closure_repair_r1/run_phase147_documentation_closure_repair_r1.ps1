$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 147 Documentation Closure Repair R1"
Write-Host "EOF normalization only"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Pytest rerun: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$Targets = @(
  "docs/development_log.md",
  "docs/roadmap.md",
  "docs/proof_records.md"
)

Write-Host ""
Write-Host "A. Verifying Phase 147 documentation is already present..."
python -c "from pathlib import Path; checks=[('docs/development_log.md','# Phase 147 — RC1 Argument-method ownership 完了'),('docs/roadmap.md','## 現在地: Phase 148 — RC2 Recursive exactness evidence exposure'),('docs/proof_records.md','# Phase 147 Argument-method ownership provenance record')]; assert all(Path(p).read_text(encoding='utf-8').count(m)==1 for p,m in checks); print('Phase 147 documentation markers before repair: PASS')"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "B. Applying EOF-only repair..."
python "$PackageDir\apply_phase147_documentation_closure_repair_r1.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "C. Diff verification..."
git diff --check -- $Targets
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "git diff --check: PASS"

Write-Host ""
Write-Host "D. Exact marker verification..."
python -c "from pathlib import Path; checks=[('docs/development_log.md','# Phase 147 — RC1 Argument-method ownership 完了'),('docs/roadmap.md','## 現在地: Phase 148 — RC2 Recursive exactness evidence exposure'),('docs/proof_records.md','# Phase 147 Argument-method ownership provenance record')]; assert all(Path(p).read_text(encoding='utf-8').count(m)==1 for p,m in checks); print('Phase 147 documentation markers: PASS')"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "E. Final regression record verification..."
python -c "from pathlib import Path; result='10314 passed in 2942.66s (0:49:02)'; assert result in Path('docs/development_log.md').read_text(encoding='utf-8'); assert result in Path('docs/roadmap.md').read_text(encoding='utf-8'); assert result in Path('docs/proof_records.md').read_text(encoding='utf-8'); print('Phase 147 final regression record: PASS')"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "F. Changed-file summary..."
git diff --numstat -- $Targets
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 147 Documentation Closure Repair R1: PASS"
Write-Host ""
Write-Host "Repair:"
Write-Host "  docs/development_log.md EOF normalized"
Write-Host "  docs/proof_records.md EOF normalized"
Write-Host ""
Write-Host "Content:"
Write-Host "  Phase 147 documentation preserved"
Write-Host "  roadmap preserved"
Write-Host ""
Write-Host "No pytest rerun."
Write-Host "Next phase after documentation closure: Phase 148 / RC2"
Write-Host "=============================================================="
