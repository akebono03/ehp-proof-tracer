$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    $env:PYTHONPATH = "$package;$root;$env:PYTHONPATH"
    python "$package\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q "$package\test_phase165_r57_r6_stable_transport_gate.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "R57-R6 stable transport connection audit passed; no production changes; full pytest NOT run."
}
finally { Pop-Location }
