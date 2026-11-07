param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OriginalPythonPath = $env:PYTHONPATH
$OriginalNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$GuardAppliedByThisRun = $false

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R17R2 git fetch failed' }

    & python -B -m phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R17R2 guarded preflight failed' }

    Write-Output 'PHASE174_R3R7R17R2_PYTEST_GROUP=PATH_CONTRACT'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
        '.\phase174_r3_r7_r17r2_windows_git_path_guard_fix\tests\test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R17R2 focused path contract failed' }

    $PriorRunner = '.\phase174_r3_r7_r17r1_historical_test_contract\run.ps1'
    if (-not (Test-Path -LiteralPath $PriorRunner)) {
        throw 'Previously extracted R17R1 run.ps1 is missing'
    }

    if ($DryRun) {
        & powershell -NoProfile -ExecutionPolicy Bypass -File $PriorRunner -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'R17R1 original DryRun failed' }
        Write-Output 'PHASE174_R3R7R17R2_GATE=PASS_PREFLIGHT_WINDOWS_PATH_CORRECTION'
    }
    else {
        $GuardAppliedByThisRun = $true
        & python -B -m phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R17R2 guarded audit correction failed' }

        Write-Output 'PHASE174_R3R7R17R2_PYTEST_GROUP=LIVE_GUARD'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r17r2_windows_git_path_guard_fix\tests\test_live_guard.py'
        if ($LASTEXITCODE -ne 0) { throw 'R17R2 live guard regression failed' }

        & powershell -NoProfile -ExecutionPolicy Bypass -File $PriorRunner
        if ($LASTEXITCODE -ne 0) { throw 'Corrected R17R1 delegated execution failed' }

        & python -B -m phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch --verify
        if ($LASTEXITCODE -ne 0) { throw 'R17R2 guard verification failed' }
        Write-Output 'PHASE174_R3R7R17R2_GATE=PASS_WINDOWS_GIT_PATH_GUARD_R17R1_FINAL'
    }
    Write-Output '(END)'
}
catch {
    $Failure = $_.ToString()
    if ($GuardAppliedByThisRun) {
        & python -B -m phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Warning 'R17R2 source-guard rollback needs manual review'
        }
    }
    throw $Failure
}
finally {
    $env:PYTHONPATH = $OriginalPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OriginalNoBytecode
    Pop-Location
}
