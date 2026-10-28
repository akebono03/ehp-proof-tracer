$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    Write-Output 'PHASE169_CLOSEOUT_R1_HELPER_PYTEST_START'
    & python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $HelperExit = $LASTEXITCODE
    Write-Output "PHASE169_CLOSEOUT_R1_HELPER_PYTEST_EXIT=$HelperExit"
    if ($HelperExit -ne 0) { exit $HelperExit }
    & python -B -m phase169_phase_closeout_r1_final_test_gate.run --repo $Repo
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
