param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) {
    throw 'Run after extracting this package in the EHP Proof Tracer root'
}

python -m phase174_r3_r6_r2_prop44_lemma54.patch --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 source/HEAD guard failed' }

python -m phase174_r3_r6_r2_prop44_lemma54.verify
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 cited source check failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R3R6R2_DRY_RUN_GATE=PASS'
    exit 0
}

python -m phase174_r3_r6_r2_prop44_lemma54.patch
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 guarded patch failed' }

python -m phase174_r3_r6_r2_prop44_lemma54.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 proof ancestry audit failed' }

python -m pytest -q `
    phase174_r3_r6_r2_prop44_lemma54/tests/test_patch.py `
    phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py `
    phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py `
    phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py `
    phase173_r4_r1_lemma54_source_bridge/tests/test_source.py `
    phase174_r3_r6_source_extension/tests/test_source.py `
    phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
    phase174_r3_r5_preflight/tests/test_audit.py `
    phase174_r3_r4_public_delta_connection/tests/test_connection.py
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 focused pytest failed' }

Write-Output 'PHASE174_R3R6R2_FOCUSED_PYTEST=PASS'
Write-Output 'PHASE174_R3R6R2_FULL_PYTEST_NOT_RUN=True'
Write-Output 'PHASE174_R3R6R2_GATE=PASS'
