$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    Write-Output 'R10ET_CLOSEOUT_R3_FOCUSED_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $TestExit = $LASTEXITCODE
    Write-Output "R10ET_CLOSEOUT_R3_FOCUSED_PYTEST_EXIT=$TestExit"
    if ($TestExit -ne 0) { exit $TestExit }
    & python -B -m phase169_r10et_closeout_r3_final_readonly_audit.audit --repo $Repo
    $AuditExit = $LASTEXITCODE
    exit $AuditExit
} finally {
    Pop-Location
}
