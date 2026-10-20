$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python ".\phase166_r3v_existing_evidence_bridge\install.py"
  if ($LASTEXITCODE -ne 0) { throw 'R3-V installation failed' }
  python -m pytest -q ".\phase166_r3v_existing_evidence_bridge\test_r3v.py" ".\phase165_r57_r7_toda45_backward_connection\test_phase165_r57_r7_toda45_backward_connection.py" ".\test_phase165_r55_nk_only_goal.py"
  if ($LASTEXITCODE -ne 0) { throw 'R3-V targeted tests failed: restore files from backup' }
  Write-Host 'R3-V targeted tests PASS; full pytest NOT run.'
} finally { Pop-Location }
