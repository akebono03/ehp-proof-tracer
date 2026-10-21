$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
  $env:PYTHONIOENCODING = "utf-8"
  python ".\phase167_r1_reference_trace\audit.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally { Pop-Location }
