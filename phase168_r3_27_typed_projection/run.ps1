$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python (Join-Path $package "apply.py")
    if ($LASTEXITCODE -ne 0) { throw "Apply failed" }
    python -m pytest -q `
      (Join-Path $package "tests\test_phase168_r3_27_typed_projection.py") `
      ".\phase168_r3_26a_after_r3_25a\tests\test_phase168_r3_26_projection.py" `
      ".\phase168_r3_25_general_exactness\tests\test_phase168_r3_25_general_exactness.py" `
      ".\phase168_r3_24_pi43_order_exactness\tests\test_phase168_r3_24_pi43.py" `
      ".\phase168_r3_23_pi43_typed_narrative\tests\test_phase168_r3_23_pi43_typed.py"
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    Write-Host "R3-27 limited tests completed; full suite NOT run."
}
finally { Pop-Location }
