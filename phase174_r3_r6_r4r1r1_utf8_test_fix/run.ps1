param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $Repo

& git fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 cannot refresh GitHub develop.' }

$Tests = @(
    'phase174_r3_r6_r4r1r1_utf8_test_fix/tests/test_r4r1r1_utf8.py',
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

& python -m phase174_r3_r6_r4r1r1_utf8_test_fix.patch --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 review guard failed.' }

if ($DryRun) {
    Write-Output 'PHASE174_R4R1R1_COLLECTION_START'
    & python -m pytest --import-mode=importlib -p no:cacheprovider --collect-only -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 collection failed.' }
    Write-Output 'PHASE174_R4R1R1_COLLECTION=PASS'
    Write-Output 'PHASE174_R4R1R1_DRYRUN_GATE=PASS'
} else {
    & python -m phase174_r3_r6_r4r1r1_utf8_test_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 test correction failed.' }
    Write-Output 'PHASE174_R4R1R1_FOCUSED_PYTEST_START'
    & python -m pytest --import-mode=importlib -p no:cacheprovider -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 focused pytest failed.' }
    Write-Output 'PHASE174_R4R1R1_FOCUSED_PYTEST=PASS'
    & python -m phase174_r3_r6_r4_common_reference.audit
    if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 public Reference audit failed.' }
    Write-Output 'PHASE174_R4R1R1_AUDIT=PASS'
    Write-Output 'PHASE174_R4R1R1_GATE=PASS'
}
Write-Output '(END)'
