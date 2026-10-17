$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($oldPythonPath) { "$project;$oldPythonPath" } else { "$project" }
    python (Join-Path $package 'install.py')
    if ($LASTEXITCODE -ne 0) { throw 'R12-R26 installation failed' }
    python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r26_map_candidates.py')
    if ($LASTEXITCODE -ne 0) { throw 'R12-R26 focused tests failed' }
    python (Join-Path $package 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R12-R26 audit failed' }
} finally {
    $env:PYTHONPATH = $oldPythonPath
    Pop-Location
}
