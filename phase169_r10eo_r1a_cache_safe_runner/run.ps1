$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$expectedHead = "57f807901f87c8d66acf4ee4db16ce05b00dccd4"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0) { throw "Cannot read Git branch" }
$head = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw "Cannot read Git HEAD" }
Write-Host "R10EO_R1A_BRANCH=$branch"
Write-Host "R10EO_R1A_HEAD=$head"
if ($branch -ne "develop") { throw "Expected develop branch" }
if ($head -ne $expectedHead) {
    throw "HEAD changed. Re-audit develop before running this fixed runner."
}

$auditFolder = Join-Path $repoRoot "phase169_r10eo_r1_definition_audit"
if (-not (Test-Path (Join-Path $auditFolder "audit.py"))) {
    throw "Original R10EO-R1 audit package is required in the repository root"
}

$watched = @(
    "data/HyoujiGen.csv",
    "phase169_r10b_registered_stable_family_binding/family_registry.py",
    "phase169_r10d2_general_family_definition/family_citation.py",
    "phase169_r10e8_hyoujigen_generic_suspension/source_records.py",
    "phase169_r10e8_hyoujigen_generic_suspension/chapter_vi_reference.py",
    "phase169_r10e1_general_group_transport/transport.py",
    "phase165_r52_r9_shared_math.py",
    "sources/toda/Toda_05_2.tex",
    "sources/toda/Toda_06_2.tex"
)

$dirtyWatchedBefore = @(& git -c core.quotePath=false diff --name-only HEAD -- $watched)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect watched files before audit" }
if ($dirtyWatchedBefore.Count -gt 0) {
    throw "Audited production files have local edits: $($dirtyWatchedBefore -join ', ')"
}

$before = @(& git -c core.quotePath=false diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect tracked changes before audit" }
$before = @($before | Where-Object { $_ -ne "" } | Sort-Object -Unique)
Write-Host "R10EO_R1A_PREEXISTING_TRACKED_DIFF=$($before -join ',')"

$runId = Get-Date -Format "yyyyMMdd_HHmmss_ffff"
$output = Join-Path $auditFolder ("output\run_r1a_" + $runId)

Write-Host "R10EO_R1A_LIMITED_TEST_START"
& python -m pytest -p no:cacheprovider -q `
    phase169_r10eo_r1_definition_audit/tests/test_r10eo_audit.py `
    phase169_r10b_registered_stable_family_binding/tests/test_r10b_registered_family.py `
    phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py `
    phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py `
    phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py
if ($LASTEXITCODE -ne 0) { throw "R10EO-R1A focused pytest failed" }

Write-Host "R10EO_R1A_AUDIT_START"
& python -m phase169_r10eo_r1_definition_audit.audit --output $output --search
if ($LASTEXITCODE -ne 0) { throw "R10EO-R1A audit failed" }

$dirtyWatchedAfter = @(& git -c core.quotePath=false diff --name-only HEAD -- $watched)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect watched files after audit" }
if ($dirtyWatchedAfter.Count -gt 0) {
    Write-Host "R10EO_R1A_DIRTY_PRODUCTION=$($dirtyWatchedAfter -join ',')"
    throw "Audited production files changed during read-only audit"
}

$after = @(& git -c core.quotePath=false diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect tracked changes after audit" }
$after = @($after | Where-Object { $_ -ne "" } | Sort-Object -Unique)
$beforeKey = (@($before) -join "`n")
$afterKey = (@($after) -join "`n")
if ($beforeKey -ne $afterKey) {
    $newlyDirty = @($after | Where-Object { $_ -cnotin $before })
    $noLongerDirty = @($before | Where-Object { $_ -cnotin $after })
    Write-Host "R10EO_R1A_NEW_TRACKED_DIFF=$($newlyDirty -join ',')"
    Write-Host "R10EO_R1A_CLEARED_TRACKED_DIFF=$($noLongerDirty -join ',')"
    Write-Host "R10EO_R1A_GIT_STATUS_START"
    & git -c core.quotePath=false status --short
    throw "Tracked working tree diff changed; review the reported paths"
}

Write-Host "R10EO_R1A_TRACKED_DIFF_UNCHANGED=True"
Write-Host "R10EO_R1A_PRODUCTION_CHANGED=False"
Write-Host "R10EO_R1A_FULL_TEST_RUN=False"
Write-Host "R10EO_R1A_OUTPUT=$output"
Write-Host "R10EO_R1A_COMPLETE=PASS"
