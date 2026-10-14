$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    $env:PYTHONPATH = "$root;$env:PYTHONPATH"
    python -m pytest -q "$package\test_phase165_r57_r9_renderer_comparison.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python "$package\audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "R57-R9 comparison completed; no production modifications; full pytest NOT run."
}
finally { Pop-Location }
