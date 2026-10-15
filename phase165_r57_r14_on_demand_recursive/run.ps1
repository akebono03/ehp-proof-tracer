$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
  python "$package\install.py"
  if ($LASTEXITCODE -ne 0) { throw "R57-R14 install failed" }
  $tests = @(
    "$package\test_phase165_r57_r14_on_demand_recursive.py",
    "$root\phase165_r57_r13_proof_order_catalog\test_phase165_r57_r13_proof_order_catalog.py",
    "$root\phase165_r57_r12_ordered_internal_transport\test_phase165_r57_r12_ordered_internal_transport.py"
  )
  foreach ($test in $tests) {
    Write-Host "Running focused pytest: $test"
    python -m pytest -q "$test"
    if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed: $test" }
  }
  Write-Host "R57-R14 targeted tests passed; full pytest NOT run."
} finally {
  Pop-Location
}
