$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $repoRoot

try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15T apply"
    Write-Host ("=" * 78)
    python (Join-Path $scriptDir "apply_phase144_6_r5_15t.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15T apply failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15T syntax/import preflight"
    Write-Host ("=" * 78)
    python -m py_compile `
      ".\toda_group_proof_narrative_aggregate_semantics.py" `
      ".\tests\test_phase144_6_r5_15t_aggregate_semantics.py" `
      (Join-Path $scriptDir "audit_phase144_6_r5_15t.py")

    python -c "import toda_group_proof_narrative_aggregate_semantics"

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15T focused tests"
    Write-Host ("=" * 78)
    pytest -q `
      ".\tests\test_phase144_6_r5_15t_aggregate_semantics.py" `
      ".\tests\test_phase144_6_r5_15m_evidence_contributions.py" `
      ".\tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15T focused tests failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15T prototype audit"
    Write-Host ("=" * 78)
    python (Join-Path $scriptDir "audit_phase144_6_r5_15t.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15T prototype audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
