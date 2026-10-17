$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R24 installation failed' }
python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r24_web_search_connection.py') (Join-Path $package 'tests/test_phase165_r12_r24_import_fix.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R24 focused pytest failed' }
# Direct script execution searches the package directory first. Include the project root.
$priorPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($priorPythonPath) { $project + [IO.Path]::PathSeparator + $priorPythonPath } else { $project }
    python (Join-Path $package 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R12-R24 Web search audit failed' }
} finally {
    $env:PYTHONPATH = $priorPythonPath
}
Write-Host 'R12-R24 Web canonical search audit recorded. Full pytest NOT run.'
