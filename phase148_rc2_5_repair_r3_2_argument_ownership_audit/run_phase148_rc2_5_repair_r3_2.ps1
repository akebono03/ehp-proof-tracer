$ErrorActionPreference="Stop"
Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Repair R3.2 - Argument ownership audit"
Write-Host "Production changes: none / Test changes: none"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
$env:PYTHONPATH=(Get-Location).Path
$env:PYTHONIOENCODING="utf-8"
python -m py_compile ".\phase148_rc2_5_repair_r3_2_argument_ownership_audit\audit_phase148_rc2_5_repair_r3_2.py"
python ".\phase148_rc2_5_repair_r3_2_argument_ownership_audit\audit_phase148_rc2_5_repair_r3_2.py" |
  Tee-Object -FilePath ".\phase148_rc2_5_repair_r3_2_argument_ownership_audit\r3_2_output.txt"
if($LASTEXITCODE -ne 0){throw "R3.2 audit failed."}
Write-Host "R3.2 audit complete. No production/test changes."
Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING
