$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$testFile = Join-Path (Join-Path $here 'tests') 'test_phase165_r12_r12_ehp_consequences.py'
$auditFile = Join-Path $here 'audit.py'
$installFile = Join-Path $here 'install.py'
$env:PYTHONPATH = "$here;$project"
$env:PYTHONIOENCODING = 'utf-8'
Push-Location $project
try {
    python $installFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R12 install failed' }
    python -m pytest -q $testFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R12 focused pytest failed' }
    python $auditFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R12 audit failed' }
    Write-Host 'R12-R12 focused checks complete. Full pytest NOT run.'
} finally {
    Pop-Location
}
