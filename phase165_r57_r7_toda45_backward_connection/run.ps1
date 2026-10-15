$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    python "$package\install.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $env:PYTHONPATH = "$root;$env:PYTHONPATH"
    python -m pytest -q "$package\test_phase165_r57_r7_toda45_backward_connection.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "R57-R7 targeted tests passed; full pytest NOT run."
}
finally { Pop-Location }
