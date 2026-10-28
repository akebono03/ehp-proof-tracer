$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    Write-Output 'R10ET_CLOSEOUT_R3A_FOCUSED_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $TestExit = $LASTEXITCODE
    Write-Output "R10ET_CLOSEOUT_R3A_FOCUSED_PYTEST_EXIT=$TestExit"
    if ($TestExit -ne 0) { exit $TestExit }
    & python -B -m phase169_r10et_closeout_r3a_committed_docs_head_fix.run
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
