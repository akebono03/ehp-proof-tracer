$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Package
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
Push-Location $Repo
try {
    Write-Host 'PHASE169_CLOSEOUT_R3B_HELPER_TESTS_START'
    & python -B -m pytest -q --tb=short -p no:cacheprovider (Join-Path $Package 'tests')
    $HelperExit = $LASTEXITCODE
    Write-Host "PHASE169_CLOSEOUT_R3B_HELPER_TESTS_EXIT=$HelperExit"
    if ($HelperExit -ne 0) { throw "R3B helper tests failed: $HelperExit" }
    & python -B (Join-Path $Package 'run.py') --repo $Repo
    $RunExit = $LASTEXITCODE
    Write-Host "PHASE169_CLOSEOUT_R3B_DOCUMENTATION_EXIT=$RunExit"
    if ($RunExit -ne 0) { throw "R3B documentation closeout failed: $RunExit" }
    Write-Host 'PHASE169_CLOSEOUT_R3B_EXIT=0'
} finally {
    Pop-Location
}
