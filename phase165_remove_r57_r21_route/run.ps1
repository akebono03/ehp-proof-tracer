$ErrorActionPreference = "Stop"
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $folder
Push-Location $project
$oldPythonPath = $env:PYTHONPATH
try {
  $env:PYTHONPATH = "$project;$oldPythonPath"
  python -m phase165_remove_r57_r21_route.install
  if ($LASTEXITCODE -ne 0) { throw "Route removal failed" }
  python -m pytest -q ".\phase165_remove_r57_r21_route\test_route.py"
  if ($LASTEXITCODE -ne 0) { throw "Targeted route regression tests failed" }
} finally {
  $env:PYTHONPATH = $oldPythonPath
  Pop-Location
}
