param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$SavedPythonPath = $env:PYTHONPATH
$SavedNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$R18R1Attempted = $false
$R18R2Attempted = $false

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R18R2 git fetch failed' }

    $Preflight = @(& python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.patch --dry-run)
    if ($LASTEXITCODE -ne 0) { throw 'R18R2 guarded preflight failed' }
    $Preflight | Write-Output
    $StatusLine = @($Preflight | Where-Object { $_ -like 'PHASE174_R3R7R18R2_PATCH=PREFLIGHT_*' })
    if ($StatusLine.Count -ne 1) { throw 'R18R2 preflight state missing' }
    $InitialState = $StatusLine[0].Substring('PHASE174_R3R7R18R2_PATCH=PREFLIGHT_'.Length)

    if ($InitialState -eq 'REVIEWED_R18_ORIGINAL') {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R18R1 reviewed EOL preflight failed' }
    }
    elseif ($InitialState -eq 'R18R1_MIXED_EOL_CORRECTED') {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --verify
        if ($LASTEXITCODE -ne 0) { throw 'Existing R18R1 state failed verification' }
    }
    elseif ($InitialState -ne 'R18R2_EVIDENCE_REVALIDATION_INSTALLED') {
        throw 'Unsupported R18R2 source state'
    }

    Write-Output 'PHASE174_R3R7R18R2_PYTEST_GROUP=RECOVERY_CONTRACT'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
        '.\phase174_r3_r7_r18r2_local_evidence_recovery\tests\test_evidence.py' `
        '.\phase174_r3_r7_r18r2_local_evidence_recovery\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R18R2 recovery contract pytest failed' }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R18R2_GATE=PASS_PREFLIGHT_LOCAL_EVIDENCE_REVALIDATION'
    }
    else {
        if ($InitialState -eq 'REVIEWED_R18_ORIGINAL') {
            $R18R1Attempted = $true
            & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --apply
            if ($LASTEXITCODE -ne 0) { throw 'R18R1 EOL source correction failed' }
        }
        if ($InitialState -ne 'R18R2_EVIDENCE_REVALIDATION_INSTALLED') {
            $R18R2Attempted = $true
            & python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.patch --apply
            if ($LASTEXITCODE -ne 0) { throw 'R18R2 evidence recovery patch failed' }
        }
        & python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.patch --verify
        if ($LASTEXITCODE -ne 0) { throw 'R18R2 source verification failed' }

        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase174_r3_r7_r18_delta_image_surjectivity\run.ps1' -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'R18 revalidated DryRun failed' }

        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase174_r3_r7_r18_delta_image_surjectivity\run.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'R18 live public audit failed' }

        Write-Output 'PHASE174_R3R7R18R2_PYTEST_GROUP=HISTORICAL_DISPLAY_CORRECTED'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase173_r4_r15r17r3r3_typed_goal_display\tests\test_open_goals.py'
        if ($LASTEXITCODE -ne 0) { throw 'Corrected historical display regression failed' }

        & python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.audit
        if ($LASTEXITCODE -ne 0) { throw 'R18R2 final public evidence verification failed' }
    }
    Write-Output '(END)'
}
catch {
    $Failure = $_
    if ($R18R2Attempted) {
        & python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.patch --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'PHASE174_R3R7R18R2_ROLLBACK=FAILED_MANUAL_REVIEW_REQUIRED'
        }
    }
    if ($R18R1Attempted) {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'PHASE174_R3R7R18R1_ROLLBACK=FAILED_MANUAL_REVIEW_REQUIRED'
        }
    }
    throw $Failure
}
finally {
    $env:PYTHONPATH = $SavedPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $SavedNoBytecode
    Pop-Location
}
