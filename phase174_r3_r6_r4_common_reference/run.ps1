param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $Repo

& git fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 failed to fetch GitHub develop.' }

$Tests = @(
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
    & python -m phase174_r3_r6_r4_common_reference.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 source guard failed.' }
    Write-Output 'PHASE174_R3R6R4_COLLECTION_START'
    & python -m pytest --import-mode=importlib --collect-only -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 focused test collection failed.' }
    Write-Output 'PHASE174_R3R6R4_COLLECTION=PASS'
    Write-Output 'PHASE174_R3R6R4_DRYRUN_GATE=PASS'
} else {
    & python -m phase174_r3_r6_r4_common_reference.patch
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 patch application failed.' }
    Write-Output 'PHASE174_R3R6R4_FOCUSED_PYTEST_START'
    & python -m pytest --import-mode=importlib -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 focused pytest failed.' }
    Write-Output 'PHASE174_R3R6R4_FOCUSED_PYTEST=PASS'
    & python -m phase174_r3_r6_r4_common_reference.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 public Reference audit failed.' }
    Write-Output 'PHASE174_R3R6R4_GATE=PASS'
}
Write-Output '(END)'
