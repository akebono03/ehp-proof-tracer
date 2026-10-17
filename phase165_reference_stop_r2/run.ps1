$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$previousPythonPath = $env:PYTHONPATH
Push-Location $root
try {
  if ([string]::IsNullOrEmpty($previousPythonPath)) {
    $env:PYTHONPATH = $root
  } else {
    $env:PYTHONPATH = "$root$([IO.Path]::PathSeparator)$previousPythonPath"
  }
  python ".\phase165_reference_stop_r2\audit.py"
  if ($LASTEXITCODE -ne 0) { throw "R2 runtime audit failed" }
  python -m pytest -q ".\phase165_reference_stop_r2\test_audit.py"
  if ($LASTEXITCODE -ne 0) { throw "R2 targeted pytest failed" }
} finally {
  $env:PYTHONPATH = $previousPythonPath
  Pop-Location
}
