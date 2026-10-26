$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Package = $PSScriptRoot
Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

Write-Host "Phase 169 R2A: registered Toda (5.2) reference body only"
Write-Host "REPOSITORY: $RepoRoot"
Write-Host "Git HEAD:"
& git rev-parse --short HEAD
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[1/4] Audit actual pi_4^2 Proof Tree and screened Citation before patch"
& python -B "$Package\audit.py" before
if ($LASTEXITCODE -ne 0) {
    Write-Host "PRE-FLIGHT FAILED. No production patch attempted."
    exit $LASTEXITCODE
}

Write-Host "[2/4] Guarded replacement of one production file"
& python -B "$Package\apply.py" install
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[3/4] Focused pytest (no full suite)"
& python -m pytest `
    "$Package\tests\test_phase169_r2a_toda52_reference_body.py" `
    ".\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py" `
    ".\tests\test_phase168_r3_4_link_bridge.py" `
    ".\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py" `
    -q --tb=short
if ($LASTEXITCODE -ne 0) {
    Write-Host "FOCUSED TEST FAILURE. To undo only this patch: python -B $Package\apply.py restore"
    exit $LASTEXITCODE
}

Write-Host "[4/4] Audit actual pi_4^2 citation body after patch"
& python -B "$Package\audit.py" after
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "PHASE169_R2A_COMPLETE: one Reference Projection file patched; full suite not run."
