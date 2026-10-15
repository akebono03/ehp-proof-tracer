$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
  python "$package\install.py"
  if ($LASTEXITCODE -ne 0) { throw "R57-R16 installation failed" }
  $tests = @(
    "$package\test_phase165_r57_r16_web_proof_order.py",
    "$root\phase165_r57_r15_ordinary_recursive_connection\test_phase165_r57_r15_ordinary_recursive_connection.py",
    "$root\phase165_r57_r14_on_demand_recursive\test_phase165_r57_r14_on_demand_recursive.py"
  )
  foreach ($test in $tests) {
    Write-Host "Running focused pytest: $test"
    python -m pytest -q "$test"
    if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed: $test" }
  }
  Write-Host "R57-R16 targeted tests passed; full pytest NOT run."
} finally {
  Pop-Location
}
