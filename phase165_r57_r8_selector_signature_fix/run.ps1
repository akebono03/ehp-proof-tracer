$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$target = Join-Path $root "phase165_r57_r8_general_specialization"
if (-not (Test-Path (Join-Path $target "installer.py"))) {
    throw "R57-R8 base package must be extracted first"
}
Copy-Item -LiteralPath (Join-Path $package "installer.py") -Destination (Join-Path $target "installer.py") -Force
Push-Location $root
try {
    python (Join-Path $package "test_phase165_r57_r8_selector_signature_fix.py")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python (Join-Path $target "installer.py")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $env:PYTHONPATH = "$root;$env:PYTHONPATH"
    python -m pytest -q (Join-Path $target "test_phase165_r57_r8_general_specialization.py")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q (Join-Path $root "phase165_r57_r7_toda45_backward_connection/test_phase165_r57_r7_toda45_backward_connection.py")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "R57-R8 selector signature fixed; targeted tests passed; full pytest NOT run."
}
finally { Pop-Location }
