$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
Write-Host 'Phase 169 R3K: model-backed Japanese map properties and cyclic-display deduplication'
Write-Host 'R3K_SCOPE: renderer-only; existing ProofSteps, citations and registry untouched'
Write-Host '[0/4] Preflight and full-function generation validation'
python -B -m phase169_r3k_narrative_localization.preflight
if ($LASTEXITCODE -ne 0) { throw "R3K_PREFLIGHT_EXIT_CODE=$LASTEXITCODE" }
Write-Host '[1/4] Guarded one-function patch and new pure projection module'
python -B -m phase169_r3k_narrative_localization.apply install
if ($LASTEXITCODE -ne 0) { throw "R3K_APPLY_EXIT_CODE=$LASTEXITCODE" }
try {
    Write-Host '[2/4] Focused model renderer, R3J and prior 1-stem tests only'
    python -B -m pytest -q `
      "phase169_r3k_narrative_localization/tests/test_phase169_r3k_narrative_localization.py" `
      "phase169_r3j_narrative_boundary_audit/tests/test_r3j_narrative_boundary_audit.py" `
      "phase168_r3_41l_reasoned_prose/tests/test_phase168_r3_41l_reasoned_prose.py"
    $code = $LASTEXITCODE
    Write-Host "R3K_FOCUSED_PYTEST_EXIT_CODE=$code"
    if ($code -ne 0) { throw "R3K_FOCUSED_PYTEST_EXIT_CODE=$code" }
    Write-Host '[3/4] Audit actual Web canonical narrative and citation map'
    python -B -m phase169_r3k_narrative_localization.audit
    $code = $LASTEXITCODE
    Write-Host "R3K_AUDIT_EXIT_CODE=$code"
    if ($code -ne 0) { throw "R3K_AUDIT_EXIT_CODE=$code" }
} catch {
    Write-Warning 'Focused test/audit failed; restoring renderer and deleting new helper module.'
    python -B -m phase169_r3k_narrative_localization.apply restore
    throw
}
Write-Host '[4/4] Complete'
Write-Host 'R3K_COMPLETE: only renderer prose and display dedup changed; full suite NOT run.'
