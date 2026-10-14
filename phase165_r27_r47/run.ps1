$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
Push-Location $project
try {
    python ".\phase165_r27_r47\apply.py"
    if ($LASTEXITCODE -ne 0) { throw 'R47 installer failed' }
    python -m pytest -q ".\phase165_r27_r47\test_installer.py"
    if ($LASTEXITCODE -ne 0) { throw 'R47 targeted tests failed' }
    Write-Output 'R27-R47 targeted tests passed; full pytest NOT run.'
} finally { Pop-Location }
