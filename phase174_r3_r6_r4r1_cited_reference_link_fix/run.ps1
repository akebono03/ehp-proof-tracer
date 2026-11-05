param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $Repo

& git fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'R4R1 failed to fetch GitHub develop.' }

$Tests = @(
    'phase174_r3_r6_r4r1_cited_reference_link_fix/tests/test_r4r1_guard.py',
    'phase174_r3_r6_r4r1_cited_reference_link_fix/tests/test_r4r1_live_binding.py',
    'phase174_r3_r6_r4_common_reference/tests/test_r3r4_patch.py',
    'phase174_r3_r6_r4_common_reference/tests/test_r3r4_reference_bodies.py',
    'phase174_r3_r6_r3r2_pytest_importmode_fix/tests/test_r3r2_importmode.py',
    'phase174_r3_r6_r3r1_scoped_guard_fix/tests/test_patch.py',
    'phase174_r3_r6_r3_common_narrative/tests/test_projection.py',
    'phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py',
    'phase174_r3_r6_source_extension/tests/test_source.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'phase172_r5_prior_reference_display/tests/test_projection.py'
)

if ($DryRun) {
    & python -m phase174_r3_r6_r4r1_cited_reference_link_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 source guard failed.' }
    Write-Output 'PHASE174_R3R6R4R1_COLLECTION_START'
    & python -m pytest --import-mode=importlib -p no:cacheprovider --collect-only -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 focused collection failed.' }
    Write-Output 'PHASE174_R3R6R4R1_COLLECTION=PASS'
    Write-Output 'PHASE174_R3R6R4R1_DRYRUN_GATE=PASS'
} else {
    & python -m phase174_r3_r6_r4r1_cited_reference_link_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 guarded application failed.' }
    Write-Output 'PHASE174_R3R6R4R1_FOCUSED_PYTEST_START'
    & python -m pytest --import-mode=importlib -p no:cacheprovider -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 focused pytest failed; gate not certified.' }
    Write-Output 'PHASE174_R3R6R4R1_FOCUSED_PYTEST=PASS'
    & python -m phase174_r3_r6_r4_common_reference.audit
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 public Reference audit failed.' }
    Write-Output 'PHASE174_R3R6R4R1_AUDIT=PASS'
    Write-Output 'PHASE174_R3R6R4R1_GATE=PASS'
}
Write-Output '(END)'
