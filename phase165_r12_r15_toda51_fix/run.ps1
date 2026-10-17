$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$installFile = Join-Path $here 'install.py'
$auditFile = Join-Path $here 'audit.py'
$testFile = Join-Path (Join-Path $here 'tests') 'test_phase165_r12_r15_toda51.py'
$env:PYTHONPATH = "$here;$project"
$env:PYTHONIOENCODING = 'utf-8'
Push-Location $project
try {
    python $installFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R15 Toda (5.1) install failed' }
    python -m pytest -q $testFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R15 focused pytest failed' }
    python $auditFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R15 audit failed' }
    Write-Host 'R12-R15 Toda (5.1) focused checks complete. Full pytest NOT run.'
} finally {
    Pop-Location
}
