$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    python "$package\install.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $env:PYTHONPATH = "$root;$env:PYTHONPATH"
    $suites = @(
        "$package\test_phase165_r57_r13_proof_order_catalog.py",
        "$root\phase165_r57_r12_ordered_internal_transport\test_phase165_r57_r12_ordered_internal_transport.py",
        "$root\phase165_r57_r11_proof_order_gate\test_phase165_r57_r11_proof_order_gate.py"
    )
    foreach ($suite in $suites) {
        if (-not (Test-Path $suite)) { throw "Missing related test: $suite" }
        Write-Host "Running focused pytest: $suite"
        python -m pytest -q "$suite"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    Write-Host "R57-R13 targeted tests passed; full pytest NOT run."
} finally {
    Pop-Location
}
