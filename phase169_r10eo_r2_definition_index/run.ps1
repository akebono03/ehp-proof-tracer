$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$acceptedHeads = @(
    "57f807901f87c8d66acf4ee4db16ce05b00dccd4",
    "40813d20e11de9946735a7058995f0ccecbca029"
)
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root

$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0) { throw "Git branch check failed" }
$head = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw "Git HEAD check failed" }
Write-Host "R10EO_R2_BRANCH=$branch"
Write-Host "R10EO_R2_HEAD=$head"
if ($branch -ne "develop") { throw "Expected develop branch" }
if ($head -notin $acceptedHeads) {
    throw "Unreviewed HEAD: re-check current GitHub develop before running R10EO-R2"
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
    "sources/toda/Toda_06_2.tex",
    "phase169_r10eo_r1_definition_audit/audit.py"
)
$productionBefore = @(& git -c core.quotePath=false diff --name-only HEAD -- $watched)
if ($LASTEXITCODE -ne 0) { throw "Cannot check watched production files" }
if ($productionBefore.Count -ne 0) {
    throw "Pre-existing edits to watched files: $($productionBefore -join ',')"
}
$before = @(& git -c core.quotePath=false diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect tracked diff" }
$before = @($before | Where-Object { $_ -ne "" } | Sort-Object -Unique)
Write-Host "R10EO_R2_PREEXISTING_TRACKED_DIFF=$($before -join ',')"

Write-Host "R10EO_R2_LIMITED_TEST_START"
& python -m pytest -p no:cacheprovider -q `
    phase169_r10eo_r2_definition_index/tests/test_r10eo_r2_index.py `
    phase169_r10eo_r1_definition_audit/tests/test_r10eo_audit.py `
    phase169_r10b_registered_stable_family_binding/tests/test_r10b_registered_family.py `
    phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py `
    phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py `
    phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py
if ($LASTEXITCODE -ne 0) { throw "R10EO-R2 limited pytest failed" }

$stamp = Get-Date -Format "yyyyMMdd_HHmmss_ffff"
$output = Join-Path $PSScriptRoot ("output\run_" + $stamp)
Write-Host "R10EO_R2_AUDIT_START"
& python -m phase169_r10eo_r2_definition_index.audit --output $output
if ($LASTEXITCODE -ne 0) { throw "R10EO-R2 audit failed" }

$productionAfter = @(& git -c core.quotePath=false diff --name-only HEAD -- $watched)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect watched files after audit" }
if ($productionAfter.Count -ne 0) {
    Write-Host "R10EO_R2_CHANGED_PRODUCTION=$($productionAfter -join ',')"
    throw "Watched source changed in read-only audit"
}
$after = @(& git -c core.quotePath=false diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect tracked diff after audit" }
$after = @($after | Where-Object { $_ -ne "" } | Sort-Object -Unique)
if (($before -join "`n") -ne ($after -join "`n")) {
    Write-Host "R10EO_R2_BEFORE=$($before -join ',')"
    Write-Host "R10EO_R2_AFTER=$($after -join ',')"
    throw "Tracked diff changed during R10EO-R2 audit"
}
Write-Host "R10EO_R2_TRACKED_DIFF_UNCHANGED=True"
Write-Host "R10EO_R2_PRODUCTION_CHANGED=False"
Write-Host "R10EO_R2_FULL_TEST_RUN=False"
Write-Host "R10EO_R2_OUTPUT=$output"
Write-Host "R10EO_R2_COMPLETE=PASS"
