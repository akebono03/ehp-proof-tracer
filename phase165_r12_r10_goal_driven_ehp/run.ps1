$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$testFile = Join-Path (Join-Path $here 'tests') 'test_phase165_r12_r10_goal_driven_ehp.py'
$auditFile = Join-Path $here 'audit.py'
$env:PYTHONPATH = "$here;$project"
$env:PYTHONIOENCODING = "utf-8"
Push-Location $project
try {
    python -m pytest -q $testFile
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
    python $auditFile
    if ($LASTEXITCODE -ne 0) { throw "Audit failed" }
    Write-Host "R12-R10 focused tests and goal-derived EHP audit finished. Full pytest NOT run."
} finally {
    Pop-Location
}
