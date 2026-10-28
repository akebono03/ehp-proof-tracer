$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0) { throw "Cannot check branch" }
$head = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw "Cannot check HEAD" }
Write-Host "R10EO_R3_BRANCH=$branch"
Write-Host "R10EO_R3_HEAD=$head"
if ($branch -ne "develop") { throw "R10EO-R3 requires develop" }
if ($head -ne "3b58b2392aa0fd4ec0247f89410a85613c8b8585") {
    throw "R10EO-R3 HEAD changed; review latest GitHub code and tests first"
}

$changedPaths = @(
    "phase169_r10d2_general_family_definition/family_citation.py",
    "phase165_r52_r9_shared_math.py"
)
$existingChanges = @(& git -c core.quotePath=false diff --name-only HEAD -- $changedPaths)
if ($LASTEXITCODE -ne 0) { throw "Cannot check preexisting source edits" }
if (@($existingChanges | Where-Object { $_ -ne "" }).Count -ne 0) {
    throw "Refusing to overwrite edited production files: $($existingChanges -join ',')"
}
$before = @(& git -c core.quotePath=false diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect tracked diff" }
$before = @($before | Where-Object { $_ -ne "" } | Sort-Object -Unique)
Write-Host "R10EO_R3_PREEXISTING_TRACKED_DIFF=$($before -join ',')"

$stamp = Get-Date -Format "yyyyMMdd_HHmmss_ffff"
$runOutput = Join-Path $PSScriptRoot ("output\run_" + $stamp)
New-Item -ItemType Directory -Path $runOutput -Force | Out-Null
$backups = Join-Path $runOutput "backups"
New-Item -ItemType Directory -Path $backups -Force | Out-Null
$originals = @{}
foreach ($sourcePath in $changedPaths) {
    $full = Join-Path $root $sourcePath
    $originals[$sourcePath] = [System.IO.File]::ReadAllBytes($full)
    $destination = Join-Path $backups ([System.IO.Path]::GetFileName($sourcePath))
    [System.IO.File]::WriteAllBytes($destination, $originals[$sourcePath])
}

try {
    Write-Host "R10EO_R3_SOURCE_PATCH_START"
    & python -m phase169_r10eo_r3_reviewed_definition_bridge.patch
    if ($LASTEXITCODE -ne 0) { throw "R10EO-R3 source patch failed" }

    Write-Host "R10EO_R3_LIMITED_TEST_START"
    & python -m pytest -p no:cacheprovider -q `
        phase169_r10eo_r3_reviewed_definition_bridge/tests/test_r10eo_r3_definition_bridge.py `
        phase169_r10eo_r2_definition_index/tests/test_r10eo_r2_index.py `
        phase169_r10eo_r1_definition_audit/tests/test_r10eo_audit.py `
        phase169_r10b_registered_stable_family_binding/tests/test_r10b_registered_family.py `
        phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py `
        phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py `
        phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py
    if ($LASTEXITCODE -ne 0) { throw "R10EO-R3 limited pytest failed" }

    $auditOutput = Join-Path $runOutput "audit"
    Write-Host "R10EO_R3_LIVE_AUDIT_START"
    & python -m phase169_r10eo_r3_reviewed_definition_bridge.audit --output $auditOutput
    if ($LASTEXITCODE -ne 0) { throw "R10EO-R3 live audit failed" }

    $after = @(& git -c core.quotePath=false diff --name-only HEAD --)
    if ($LASTEXITCODE -ne 0) { throw "Cannot inspect tracked diff after R3" }
    $after = @($after | Where-Object { $_ -ne "" } | Sort-Object -Unique)
    $expected = @($before + $changedPaths | Sort-Object -Unique)
    if (($after -join "`n") -ne ($expected -join "`n")) {
        Write-Host "R10EO_R3_TRACKED_BEFORE=$($before -join ',')"
        Write-Host "R10EO_R3_TRACKED_AFTER=$($after -join ',')"
        throw "Unexpected tracked file modified during R10EO-R3"
    }
    Write-Host "R10EO_R3_EXPECTED_PRODUCTION_FILES=$($changedPaths -join ',')"
    Write-Host "R10EO_R3_FULL_TEST_RUN=False"
    Write-Host "R10EO_R3_OUTPUT=$runOutput"
    Write-Host "R10EO_R3_COMPLETE=PASS"
}
catch {
    foreach ($sourcePath in $changedPaths) {
        [System.IO.File]::WriteAllBytes((Join-Path $root $sourcePath), $originals[$sourcePath])
        Write-Host "R10EO_R3_ROLLED_BACK=$sourcePath"
    }
    throw
}
