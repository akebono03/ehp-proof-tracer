$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Finalization Repair R1"
Write-Host "Local-contract snapshot + focused failure reproduction"
Write-Host "=============================================================="
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  python ".\phase150_finalization_repair_r1\collect_phase150_finalization_repair_r1.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "R1 completed."
Write-Host "Please provide these two files:"
Write-Host "  .\phase150_finalization_repair_r1\local_snapshot\REPORT.txt"
Write-Host "  .\phase150_finalization_repair_r1\local_snapshot\focused_pytest.txt"
Write-Host ""
Write-Host "If needed, the copied local source/test files are under local_snapshot."
