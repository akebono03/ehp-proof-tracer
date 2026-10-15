$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $folder
$env:PYTHONPATH = "$folder;$project"
Push-Location $project
try {
    python -m pytest -q "$folder\test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R5-R12 focused audit tests failed.' }
    python "$folder\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R5-R12 local R5-R11 preconditions failed. Application source unchanged.' }
    Write-Host 'R5-R12 function-level retirement decision recorded. No application files modified; full pytest NOT run.'
}
finally { Pop-Location }
