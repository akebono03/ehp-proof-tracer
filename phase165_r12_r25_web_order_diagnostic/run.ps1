$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($oldPythonPath) { "$project;$oldPythonPath" } else { "$project" }
    python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r25_web_order_diagnostic.py')
    if ($LASTEXITCODE -ne 0) { throw 'R12-R25 focused pytest failed' }
    python -m phase165_r12_r25_web_order_diagnostic.audit
    if ($LASTEXITCODE -ne 0) { throw 'R12-R25 audit failed' }
} finally {
    $env:PYTHONPATH = $oldPythonPath
    Pop-Location
}
