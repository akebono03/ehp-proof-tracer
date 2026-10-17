$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$oldPythonPath = $env:PYTHONPATH
Push-Location $project
try {
  $env:PYTHONPATH = $package + [IO.Path]::PathSeparator + $project + [IO.Path]::PathSeparator + $oldPythonPath
  python -m pytest -q "$package\test_audit.py"
  if ($LASTEXITCODE -ne 0) { throw 'R12-R32 targeted pytest failed' }
  python "$package\audit.py"
  if ($LASTEXITCODE -ne 0) { throw 'R12-R32 audit failed' }
} finally {
  $env:PYTHONPATH = $oldPythonPath
  Pop-Location
}
