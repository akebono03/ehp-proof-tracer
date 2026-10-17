$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$installer = Join-Path $here 'install.py'
$tests = Join-Path (Join-Path $here 'tests') 'test_phase165_r12_r13_kernel_image.py'
$audit = Join-Path $here 'audit.py'
$env:PYTHONPATH = "$project;$here"
$env:PYTHONIOENCODING = 'utf-8'
Push-Location $project
try {
    python $installer
    if ($LASTEXITCODE -ne 0) { throw 'R12-R13 install failed' }
    python -m pytest -q $tests
    if ($LASTEXITCODE -ne 0) { throw 'R12-R13 focused pytest failed' }
    python $audit
    if ($LASTEXITCODE -ne 0) { throw 'R12-R13 audit failed' }
    Write-Host 'R12-R13 focused checks complete. Full pytest NOT run.'
} finally {
    Pop-Location
}
