$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$oldPythonPath = $env:PYTHONPATH
$oldEncoding = $env:PYTHONIOENCODING
Push-Location $repo
try {
  $env:PYTHONIOENCODING = "utf-8"
  $env:PYTHONPATH = $repo
  if ($oldPythonPath) {
    $env:PYTHONPATH = $repo + [System.IO.Path]::PathSeparator + $oldPythonPath
  }
  python ".\phase167_r1_reference_trace_fix\audit.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Dynamic audit failed with exit code $LASTEXITCODE"
  }
} finally {
  $env:PYTHONPATH = $oldPythonPath
  $env:PYTHONIOENCODING = $oldEncoding
  Pop-Location
}
