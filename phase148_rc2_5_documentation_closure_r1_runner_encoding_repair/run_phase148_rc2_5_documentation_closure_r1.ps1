$ErrorActionPreference="Stop"

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Documentation Closure R1"
Write-Host "Runner encoding repair only"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Repository-wide pytest: NOT rerun"
Write-Host "=============================================================="

$env:PYTHONIOENCODING="utf-8"

Write-Host ""
Write-Host "A. Updating five documentation files..."
python ".\phase148_rc2_5_documentation_closure_r1_runner_encoding_repair\apply_phase148_rc2_5_documentation_closure.py"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "B. Documentation UTF-8 preflight..."
python -c "from pathlib import Path; files=[Path('README.md'),Path('docs/design.md'),Path('docs/development_log.md'),Path('docs/roadmap.md'),Path('docs/proof_records.md')]; [f.read_text(encoding='utf-8') for f in files]; print('Five documentation files: UTF-8 read PASS')"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "C. Phase 148 closure marker verification..."
python -c "from pathlib import Path; checks=[('README.md','Phase 148 closure'),('docs/design.md','Phase 148'),('docs/development_log.md','Phase 148'),('docs/roadmap.md','Phase 148'),('docs/proof_records.md','Phase 148 recursive exactness exposure')]; missing=[f'{p}: {m}' for p,m in checks if m not in Path(p).read_text(encoding='utf-8')]; assert not missing, 'Missing markers: ' + '; '.join(missing); print('Phase 148 closure markers: PASS')"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "D. Full-document copy verification..."
python -c "from pathlib import Path; root=Path('phase148_rc2_5_documentation_closure')/'updated_full_documents'; files=[Path('README.md'),Path('docs/design.md'),Path('docs/development_log.md'),Path('docs/roadmap.md'),Path('docs/proof_records.md')]; missing=[str(root/f) for f in files if not (root/f).exists()]; assert not missing, 'Missing full-document copies: ' + ', '.join(missing); print('Full updated document copies: PASS')"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 148 documentation closure: PASS"
Write-Host "Phase 148 / RC2: COMPLETE"
Write-Host "Next: Phase 149 / RC3 Narrative ordering"
Write-Host "Repository-wide pytest: NOT rerun"
Write-Host "=============================================================="

Remove-Item Env:PYTHONIOENCODING
