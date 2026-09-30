$ErrorActionPreference="Stop"
Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Repair R3.1 - closure edge audit repair"
Write-Host "Production changes: none / Test changes: none"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
$env:PYTHONPATH=(Get-Location).Path
$env:PYTHONIOENCODING="utf-8"
python -m py_compile ".\phase148_rc2_5_repair_r3_1_closure_edge_audit\audit_phase148_rc2_5_repair_r3_1.py"
python ".\phase148_rc2_5_repair_r3_1_closure_edge_audit\audit_phase148_rc2_5_repair_r3_1.py" | Tee-Object -FilePath ".\phase148_rc2_5_repair_r3_1_closure_edge_audit\r3_1_output.txt"
if($LASTEXITCODE -ne 0){throw "R3.1 audit failed."}
Write-Host "R3.1 audit complete. No production/test changes."
Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING
