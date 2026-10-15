$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    python "$package\installer.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $env:PYTHONPATH = "$root;$env:PYTHONPATH"
    python -m pytest -q "$package\test_phase165_r57_r8_general_specialization.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q "$root\phase165_r57_r7_toda45_backward_connection\test_phase165_r57_r7_toda45_backward_connection.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "R57-R8 targeted tests passed; full pytest NOT run."
}
finally { Pop-Location }
