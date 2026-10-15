$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    python "$package\install.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$package\update_regression_test.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $env:PYTHONPATH = "$root;$env:PYTHONPATH"
    $suites = @(
        "$package\test_phase165_r57_r11_proof_order_gate.py",
        "$root\phase165_r57_r10_proofstep_fidelity\test_phase165_r57_r10_proofstep_fidelity.py",
        "$root\phase165_r57_r8_general_specialization\test_phase165_r57_r8_general_specialization.py",
        "$root\phase165_r57_r7_toda45_backward_connection\test_phase165_r57_r7_toda45_backward_connection.py"
    )
    foreach ($suite in $suites) {
        Write-Host "Running focused pytest: $suite"
        python -m pytest -q "$suite"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    Write-Host "R57-R11 targeted tests passed; full pytest NOT run."
} finally {
    Pop-Location
}
