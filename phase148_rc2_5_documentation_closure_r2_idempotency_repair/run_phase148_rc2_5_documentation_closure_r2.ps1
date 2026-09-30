$ErrorActionPreference="Stop"

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Documentation Closure R2"
Write-Host "Idempotency-marker repair"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Repository-wide pytest: NOT rerun"
Write-Host "=============================================================="

$env:PYTHONIOENCODING="utf-8"

Write-Host ""
Write-Host "A. Applying repaired documentation updater..."
python ".\phase148_rc2_5_documentation_closure_r2_idempotency_repair\apply_phase148_rc2_5_documentation_closure_r2.py"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "B. Verifying exact unique closure headings..."
python -c "from pathlib import Path; checks=[('README.md','## Phase 148 closure — recursive exactness evidence exposure'),('docs/design.md','# Phase 148 設計完了記録 — Recursive exactness evidence exposure'),('docs/development_log.md','# Phase 148 完了 — RC2 Recursive exactness evidence exposure'),('docs/roadmap.md','# Phase 148 完了後ロードマップ'),('docs/proof_records.md','# Phase 148 recursive exactness exposure / provenance record')]; missing=[p for p,m in checks if m not in Path(p).read_text(encoding='utf-8')]; duplicates=[p for p,m in checks if Path(p).read_text(encoding='utf-8').count(m)!=1]; assert not missing, 'Missing closure headings: '+', '.join(missing); assert not duplicates, 'Duplicate closure headings: '+', '.join(duplicates); print('Five exact unique Phase 148 closure headings: PASS')"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "C. UTF-8 and full-document copy verification..."
python -c "from pathlib import Path; files=[Path('README.md'),Path('docs/design.md'),Path('docs/development_log.md'),Path('docs/roadmap.md'),Path('docs/proof_records.md')]; [f.read_text(encoding='utf-8') for f in files]; root=Path('phase148_rc2_5_documentation_closure')/'updated_full_documents'; missing=[str(root/f) for f in files if not (root/f).exists()]; assert not missing, 'Missing copies: '+', '.join(missing); print('UTF-8 and full-document copies: PASS')"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 148 documentation closure: PASS"
Write-Host "Phase 148 / RC2: COMPLETE"
Write-Host "Next: Phase 149 / RC3 Narrative ordering"
Write-Host "Repository-wide pytest: NOT rerun"
Write-Host "=============================================================="

Remove-Item Env:PYTHONIOENCODING
