$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python (Join-Path $package "apply.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-26a apply failed" }
    python -m pytest -q `
      (Join-Path $package "tests\test_phase168_r3_26_projection.py") `
      ".\phase168_r3_25a_exactness_latex_fix\tests\test_phase168_r3_25a_exactness_latex.py" `
      ".\phase168_r3_25_general_exactness\tests\test_phase168_r3_25_general_exactness.py" `
      ".\phase168_r3_24_pi43_order_exactness\tests\test_phase168_r3_24_pi43.py" `
      ".\phase168_r3_23_pi43_typed_narrative\tests\test_phase168_r3_23_pi43_typed.py"
    if ($LASTEXITCODE -ne 0) { throw "R3-26a limited pytest failed" }
    Write-Host "R3-26a limited validation completed; full suite NOT run."
}
finally { Pop-Location }
