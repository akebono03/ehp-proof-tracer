$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$testFile = Join-Path (Join-Path $here 'tests') 'test_phase165_r12_r11_prop42_unified.py'
$installer = Join-Path $here 'install.py'
$env:PYTHONPATH = "$project;$here"
$env:PYTHONIOENCODING = 'utf-8'
Push-Location $project
try {
    python $installer
    if ($LASTEXITCODE -ne 0) { throw 'R12-R11 installation failed' }
    python -m pytest -q $testFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R11 focused pytest failed' }
    Write-Host 'R12-R11 installed and focused tests passed. Full pytest NOT run.'
} finally {
    Pop-Location
}
