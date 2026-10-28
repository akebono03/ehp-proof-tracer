$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    Write-Output 'PHASE169_CLOSEOUT_R4A_HELPER_TESTS_START'
    & python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $TestCode = $LASTEXITCODE
    Write-Output "PHASE169_CLOSEOUT_R4A_HELPER_TESTS_EXIT=$TestCode"
    if ($TestCode -ne 0) { throw "R4A helper tests failed: $TestCode" }
    & python -B -m phase169_phase_closeout_r4a_committed_document_audit.run --repo $Repo
    $RunCode = $LASTEXITCODE
    if ($RunCode -ne 0) { throw "R4A read-only audit failed: $RunCode" }
} finally {
    Pop-Location
}
