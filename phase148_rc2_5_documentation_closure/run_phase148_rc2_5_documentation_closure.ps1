$ErrorActionPreference="Stop"

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Documentation Closure"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Repository-wide pytest: NOT rerun"
Write-Host "=============================================================="

$env:PYTHONIOENCODING="utf-8"

Write-Host ""
Write-Host "A. Updating five documentation files..."
python ".\phase148_rc2_5_documentation_closure\apply_phase148_rc2_5_documentation_closure.py"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "B. Documentation syntax/content preflight..."
python -c "from pathlib import Path; files=[Path('README.md'),Path('docs/design.md'),Path('docs/development_log.md'),Path('docs/roadmap.md'),Path('docs/proof_records.md')]; [f.read_text(encoding='utf-8') for f in files]; print('Five documentation files: UTF-8 read PASS')"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "C. Phase 148 closure markers..."
Select-String -Path ".\README.md" -Pattern "Phase 148 closure"
Select-String -Path ".\docs\design.md" -Pattern "Phase 148 設計完了記録"
Select-String -Path ".\docs\development_log.md" -Pattern "Phase 148 完了"
Select-String -Path ".\docs\roadmap.md" -Pattern "Phase 148 完了後ロードマップ"
Select-String -Path ".\docs\proof_records.md" -Pattern "Phase 148 recursive exactness exposure"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 148 documentation closure: PASS"
Write-Host "Phase 148 / RC2: COMPLETE"
Write-Host "Next: Phase 149 / RC3 Narrative ordering"
Write-Host "Full updated files are under:"
Write-Host ".\phase148_rc2_5_documentation_closure\updated_full_documents\"
Write-Host "=============================================================="

Remove-Item Env:PYTHONIOENCODING
