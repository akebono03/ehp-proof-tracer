param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
$AppliedByThisRun = $false

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R18R1 git fetch failed' }

    & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R18R1 reviewed Source Guard preflight failed' }

    Write-Output 'PHASE174_R3R7R18R1_PYTEST_GROUP=GUARD_CONTRACT'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
        '.\phase174_r3_r7_r18r1_git_mixed_eol_guard\tests\test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R18R1 guard contract pytest failed' }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R18R1_GATE=PASS_PREFLIGHT_MIXED_EOL_GUARD'
    }
    else {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R18R1 reviewed audit correction failed' }
        $AppliedByThisRun = $true

        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase174_r3_r7_r18_delta_image_surjectivity\run.ps1' -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'R18 corrected DryRun failed' }

        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase174_r3_r7_r18_delta_image_surjectivity\run.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'R18 corrected public audit failed' }

        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --verify
        if ($LASTEXITCODE -ne 0) { throw 'R18R1 final source verification failed' }
        Write-Output 'PHASE174_R3R7R18R1_GATE=PASS_REVIEWED_GIT_MIXED_EOL_R18_PUBLIC'
    }
    Write-Output '(END)'
}
catch {
    $Failure = $_
    if ($AppliedByThisRun) {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'PHASE174_R3R7R18R1_ROLLBACK=FAILED_MANUAL_REVIEW_REQUIRED'
        }
    }
    throw $Failure
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    Pop-Location
}
