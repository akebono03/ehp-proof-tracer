param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) {
    throw 'Execute from the extracted package inside ehp_proof repository'
}

python -m phase174_r3_r6_source_extension.patch --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 source/HEAD DryRun failed' }

python -m phase174_r3_r6_source_extension.verify
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 adopted Toda source verification failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R3R6_DRY_RUN_GATE=PASS'
    exit 0
}

python -m phase174_r3_r6_source_extension.patch
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 guarded patch failed' }

python -m phase174_r3_r6_source_extension.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 source ancestry audit failed' }

python -m pytest -q `
    phase174_r3_r6_source_extension/tests/test_source.py `
    phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
    phase174_r3_r5_preflight/tests/test_audit.py `
    phase174_r3_r4_public_delta_connection/tests/test_connection.py
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 focused pytest failed' }

Write-Output 'PHASE174_R3R6_FOCUSED_PYTEST=PASS'
Write-Output 'PHASE174_R3R6_FULL_PYTEST_NOT_RUN=True'
Write-Output 'PHASE174_R3R6_GATE=PASS'
