$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $folder
$env:PYTHONPATH = "$folder;$project"
Push-Location $project
try {
    python -m pytest -q "$folder\test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R5-R13 focused audit unit tests failed.' }
    python "$folder\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R5-R13 preconditions failed. No application files changed.' }
    Write-Host 'R5-R13 comparison evidence saved. Legacy Narrative NOT retired. Full pytest NOT run.'
}
finally { Pop-Location }
