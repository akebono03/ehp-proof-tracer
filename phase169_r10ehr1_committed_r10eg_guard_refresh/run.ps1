$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Audit = Join-Path $Repo 'phase169_r10eh_stem6_10_11_14_audit'
$Original = Join-Path $Audit 'run.ps1'
$Stage = Join-Path $Audit 'run_r1_verified.ps1'
$ReviewedRunner = Join-Path $Package 'payload\run_r1.ps1'
$OriginalSHA = 'f6a5af06f75121b84b3ff6b77266b36c057ee7f35619c75c6a80f68068159462'
$ReviewedSHA = 'b56d68356c5c7b813bb7cffa7f42ec44045068a350d5df84d88d05fc8ec3c578'
if (-not (Test-Path -LiteralPath $Original -PathType Leaf)) {
    throw 'R10EH original runner missing: extract phase169_r10eh_stem6_10_11_14_audit.zip first'
}
$Detected = (Get-FileHash -LiteralPath $Original -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Detected -ne $OriginalSHA) {
    throw 'R10EH original runner differs from reviewed input; refusing unsafe replacement'
}
if ((Get-FileHash -LiteralPath $ReviewedRunner -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ReviewedSHA) {
    throw 'R10EH-R1 reviewed runner payload hash mismatch'
}
if (Test-Path -LiteralPath $Stage) {
    throw 'R10EH-R1 temporary runner path is occupied; no file was replaced'
}
$Branch = (& git -C $Repo branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
    throw 'R10EH-R1 requires local develop branch'
}
$Head = (& git -C $Repo rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'R10EH-R1 unable to read HEAD' }
Write-Host "R10EHR1_BRANCH=$Branch"
Write-Host "R10EHR1_HEAD=$Head"
Write-Host 'R10EHR1_MODE=AUDIT_ONLY_GUARD_REFRESH'
Write-Host 'R10EHR1_ORIGINAL_RUNNER_UNCHANGED=True'
Push-Location $Repo
try {
    & python -B -m pytest -q -p no:cacheprovider '.\phase169_r10ehr1_committed_r10eg_guard_refresh\tests\test_r10ehr1_guard.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EH-R1 guard tests failed' }
    Copy-Item -LiteralPath $ReviewedRunner -Destination $Stage -ErrorAction Stop
    try {
        & powershell -NoProfile -ExecutionPolicy Bypass -File $Stage
        if ($LASTEXITCODE -ne 0) {
            throw "R10EH-R1 delegated R10EH audit failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        if (Test-Path -LiteralPath $Stage) {
            if ((Get-FileHash -LiteralPath $Stage -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ReviewedSHA) {
                throw 'R10EH-R1 staged runner was unexpectedly modified; preserving it for inspection'
            }
            Remove-Item -LiteralPath $Stage -Force
        }
    }
    Write-Host 'R10EHR1_ORIGINAL_RUNNER_UNCHANGED=PASS'
    Write-Host 'R10EHR1_REVIEWED_R10EG_BLOB=PASS'
    Write-Host 'R10EHR1_DELEGATED_R10EH_AUDIT=PASS'
    Write-Host 'R10EHR1_FULL_PYTEST_RUN=False'
}
finally {
    Pop-Location
}
