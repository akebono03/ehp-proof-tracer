$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python ".\phase166_r3v_test_repair\install.py"
  if ($LASTEXITCODE -ne 0) { throw 'Test patch failed' }
  python -m pytest -q ".\phase166_r3v_existing_evidence_bridge\test_r3v.py" ".\phase165_r57_r7_toda45_backward_connection\test_phase165_r57_r7_toda45_backward_connection.py" ".\test_phase165_r55_nk_only_goal.py"
  if ($LASTEXITCODE -ne 0) { throw 'R3-V targeted tests remain failing' }
  Write-Host 'R3-V targeted tests PASS; production code unchanged by this repair; full pytest NOT run.'
} finally { Pop-Location }
