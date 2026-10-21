$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
  $env:PYTHONPATH = $repo
  $env:PYTHONIOENCODING = "utf-8"
  python ".\phase167_r3_duplicate_given_fix\apply.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  Copy-Item ".\phase167_r3_duplicate_given_fix\test_phase167_r3_duplicate_given.py" ".\tests\test_phase167_r3_duplicate_given.py" -Force
  python -m pytest -q tests/test_phase167_r3_duplicate_given.py tests/test_phase167_r3_generic_resolver.py
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally { Pop-Location }
