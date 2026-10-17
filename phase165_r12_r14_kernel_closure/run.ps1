$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$testFile = Join-Path (Join-Path $here 'tests') 'test_phase165_r12_r14_kernel_closure.py'
$auditFile = Join-Path $here 'audit.py'
$env:PYTHONPATH = "$here;$project"
$env:PYTHONIOENCODING = 'utf-8'
Push-Location $project
try {
    python $auditFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R14 audit failed' }
    python -m pytest -q $testFile
    if ($LASTEXITCODE -ne 0) { throw 'R12-R14 focused pytest failed; inspect audit_result.json' }
    Write-Host 'R12-R14 recursive kernel proof verified. Full pytest NOT run.'
} finally {
    Pop-Location
}
