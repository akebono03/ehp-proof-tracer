param(
    [switch]$Commit
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    Write-Output 'PHASE169_CLOSEOUT_R4_HELPER_TESTS_START'
    & python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $TestCode = $LASTEXITCODE
    Write-Output "PHASE169_CLOSEOUT_R4_HELPER_TESTS_EXIT=$TestCode"
    if ($TestCode -ne 0) { throw "R4 helper tests failed: $TestCode" }
    $ArgList = @('-B', '-m', 'phase169_phase_closeout_r4_safe_docs_commit.run', '--repo', $Repo)
    if ($Commit) { $ArgList += '--commit' }
    & python @ArgList
    $RunCode = $LASTEXITCODE
    if ($RunCode -ne 0) { throw "R4 audit/commit failed: $RunCode" }
} finally {
    Pop-Location
}
