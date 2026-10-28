$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$expectedHead = "57f807901f87c8d66acf4ee4db16ce05b00dccd4"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$branch = (& git branch --show-current).Trim()
$head = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw "Cannot read Git HEAD" }
Write-Host "R10EO_BRANCH=$branch"
Write-Host "R10EO_HEAD=$head"
if ($branch -ne "develop") { throw "Expected develop branch" }
if ($head -ne $expectedHead) {
    throw "HEAD changed. Re-audit GitHub develop and refresh this audit package before running."
}

# Existing uncommitted edits to audited production files invalidate the review.
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
$dirtyWatched = @(& git diff --name-only HEAD -- $watched)
if ($dirtyWatched.Count -gt 0) {
    throw "Audited production files have local edits: $($dirtyWatched -join ', ')"
}

$before = @(& git diff --name-only HEAD --)
$runId = Get-Date -Format "yyyyMMdd_HHmmss_ffff"
$output = Join-Path $PSScriptRoot ("output\run_" + $runId)

Write-Host "R10EO_LIMITED_TEST_START"
& python -m pytest -q `
  phase169_r10eo_r1_definition_audit/tests/test_r10eo_audit.py `
  phase169_r10b_registered_stable_family_binding/tests/test_r10b_registered_family.py `
  phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py `
  phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py `
  phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py
if ($LASTEXITCODE -ne 0) { throw "R10EO focused pytest failed" }

Write-Host "R10EO_AUDIT_START"
& python -m phase169_r10eo_r1_definition_audit.audit --output $output --search
if ($LASTEXITCODE -ne 0) { throw "R10EO audit failed" }

$after = @(& git diff --name-only HEAD --)
if ((@($before | Sort-Object) -join "`n") -ne (@($after | Sort-Object) -join "`n")) {
    throw "Tracked working tree diff changed during read-only audit"
}
Write-Host "R10EO_PRODUCTION_CHANGED=False"
Write-Host "R10EO_FULL_TEST_RUN=False"
Write-Host "R10EO_OUTPUT=$output"
Write-Host "R10EO_COMPLETE=PASS"
