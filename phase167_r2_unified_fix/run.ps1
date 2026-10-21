$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
  $env:PYTHONPATH = $repo
  python ".\phase167_r2_unified_fix\apply.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python -m pytest -q tests/test_phase167_r2_unified_reference.py tests/test_phase167_r2_shared_reference.py tests/test_phase144_6_r3_structured_references.py
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
  Pop-Location
}
