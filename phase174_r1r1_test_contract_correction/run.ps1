param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedHead = 'cb85913905b2f7452bda2a2c4428e6fe5a3a793a'
$OriginalTestBlob = '5b3760fbc0797a81ea41af1f0cd1dbfe3b7afac3'
$ReplacementTestBlob = '9def7480a529ab5f6c2e344866016cf36330a409'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Destination = Join-Path $Root 'test_phase165_r55_nk_only_goal.py'
$Replacement = Join-Path $PSScriptRoot 'replacement\test_phase165_r55_nk_only_goal.py'
$OriginalRunner = Join-Path $Root 'phase174_r1_goal_audit\run.ps1'

Set-Location $Root

if (-not (Test-Path -LiteralPath $OriginalRunner)) {
    throw 'The original Phase 174 R1 audit package must be extracted first.'
}
if (-not (Test-Path -LiteralPath $Replacement)) {
    throw 'Missing full replacement test file.'
}

$Branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
    throw 'This correction requires the local develop branch.'
}
$LocalHead = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $LocalHead -ne $ExpectedHead) {
    throw "The local HEAD has changed; review it before applying this correction."
}
$RemoteLine = @(& git ls-remote origin refs/heads/develop)
if ($LASTEXITCODE -ne 0 -or $RemoteLine.Count -ne 1) {
    throw 'Cannot resolve remote develop.'
}
$RemoteHead = (($RemoteLine[0].Trim()) -split '\s+')[0]
if ($RemoteHead -ne $ExpectedHead) {
    throw 'Remote develop has changed; review the new source before applying.'
}

$CommittedBlob = (& git rev-parse 'HEAD:test_phase165_r55_nk_only_goal.py').Trim()
if ($LASTEXITCODE -ne 0 -or $CommittedBlob -ne $OriginalTestBlob) {
    throw 'The committed old test is not the reviewed version.'
}
$ActualBlob = (& git hash-object -- "$Destination").Trim()
if ($LASTEXITCODE -ne 0) {
    throw 'Cannot hash local old test file.'
}
$PackageBlob = (& git hash-object -- "$Replacement").Trim()
if ($LASTEXITCODE -ne 0 -or $PackageBlob -ne $ReplacementTestBlob) {
    throw 'Replacement package content is not the reviewed test.'
}

$StagedPaths = @(& git diff --cached --name-only)
if ($LASTEXITCODE -ne 0) {
    throw 'Cannot check Git index.'
}
if ($StagedPaths -contains 'test_phase165_r55_nk_only_goal.py') {
    throw 'The existing test has staged changes; the correction will not overwrite it.'
}

$AlreadyInstalled = $ActualBlob -eq $ReplacementTestBlob
if (-not $AlreadyInstalled -and $ActualBlob -ne $OriginalTestBlob) {
    throw 'The test was edited locally; refusing to overwrite user changes.'
}

Write-Output "PHASE174_R1R1_HEAD=$LocalHead"
Write-Output 'PHASE174_R1R1_REVIEWED_OLD_TEST=PASS'
Write-Output 'PHASE174_R1R1_REPLACEMENT_CONTENT=PASS'
Write-Output "PHASE174_R1R1_ALREADY_INSTALLED=$AlreadyInstalled"

# The original R1 preflight validates its reviewed production sources.
& powershell -NoProfile -ExecutionPolicy Bypass -File "$OriginalRunner" -DryRun
if ($LASTEXITCODE -ne 0) {
    throw 'Original R1 preflight failed.'
}

if ($DryRun) {
    Write-Output 'PHASE174_R1R1_DRY_RUN=PASS'
    Write-Output 'PHASE174_R1R1_NO_FILES_CHANGED=True'
    exit 0
}

$IndexBefore = @(& git ls-files --stage) -join "`n"
if ($LASTEXITCODE -ne 0) {
    throw 'Cannot snapshot index before correction.'
}

if (-not $AlreadyInstalled) {
    Copy-Item -LiteralPath "$Replacement" -Destination "$Destination"
}
$InstalledBlob = (& git hash-object -- "$Destination").Trim()
if ($LASTEXITCODE -ne 0 -or $InstalledBlob -ne $ReplacementTestBlob) {
    throw 'Corrected test was not installed with the expected bytes.'
}
Write-Output 'PHASE174_R1R1_TEST_INSTALLED=PASS'

# Re-run the original R1 audit and all its focused tests, including the
# corrected legacy test; do not omit or deselect its four failing cases.
& powershell -NoProfile -ExecutionPolicy Bypass -File "$OriginalRunner"
if ($LASTEXITCODE -ne 0) {
    throw 'Re-run of Phase 174 R1 failed.'
}

$IndexAfter = @(& git ls-files --stage) -join "`n"
if ($LASTEXITCODE -ne 0 -or $IndexBefore -cne $IndexAfter) {
    throw 'Git index changed during correction.'
}
Write-Output 'PHASE174_R1R1_GIT_INDEX_PRESERVED=PASS'
Write-Output 'PHASE174_R1R1_GATE=PASS'
