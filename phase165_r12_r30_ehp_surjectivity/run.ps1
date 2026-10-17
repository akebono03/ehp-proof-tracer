$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
$previous = $env:PYTHONPATH
try {
  $env:PYTHONPATH = $project + [IO.Path]::PathSeparator + $previous
  python "$package\install.py"
  if ($LASTEXITCODE -ne 0) { throw "R12-R30 installation failed" }
  python -m pytest -q "$package\test_phase165_r12_r30_ehp_surjectivity.py" "tests\test_phase165_r12_r2_quotient_rules.py"
  if ($LASTEXITCODE -ne 0) { throw "R12-R30 targeted tests failed" }
  python "$package\audit.py"
  if ($LASTEXITCODE -ne 0) { throw "R12-R30 audit failed" }
} finally {
  $env:PYTHONPATH = $previous
  Pop-Location
}
