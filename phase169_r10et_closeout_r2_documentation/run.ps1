$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    Write-Output 'R10ET_CLOSEOUT_R2_FOCUSED_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $TestExit = $LASTEXITCODE
    Write-Output "R10ET_CLOSEOUT_R2_FOCUSED_PYTEST_EXIT=$TestExit"
    if ($TestExit -ne 0) { exit $TestExit }
    & python -B (Join-Path $PSScriptRoot 'update_docs.py') --repo $Repo
    $PatchExit = $LASTEXITCODE
    exit $PatchExit
} finally {
    Pop-Location
}
