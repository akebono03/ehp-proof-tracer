$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
  $env:PYTHONPATH = $repo
  $env:PYTHONIOENCODING = "utf-8"
  python ".\phase167_r3_goal_position_audit\audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python -m pytest -q tests/test_phase165_r12_r2_quotient_rules.py
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
  Pop-Location
}
