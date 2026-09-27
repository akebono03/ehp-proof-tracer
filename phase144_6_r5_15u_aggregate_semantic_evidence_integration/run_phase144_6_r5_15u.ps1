$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $repoRoot

try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15U apply"
    Write-Host ("=" * 78)
    python (Join-Path $scriptDir "apply_phase144_6_r5_15u.py")
    Copy-Item `
      (Join-Path $scriptDir "tests\test_phase144_6_r5_15u_evidence_integration.py") `
      ".\tests\test_phase144_6_r5_15u_evidence_integration.py" `
      -Force

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15U syntax/import preflight"
    Write-Host ("=" * 78)
    python -m py_compile `
      ".\toda_group_proof_narrative_evidence_contributions.py" `
      ".\tests\test_phase144_6_r5_15u_evidence_integration.py" `
      (Join-Path $scriptDir "audit_phase144_6_r5_15u.py")

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15U focused tests"
    Write-Host ("=" * 78)
    pytest -q `
      ".\tests\test_phase144_6_r5_15u_evidence_integration.py" `
      ".\tests\test_phase144_6_r5_15t_aggregate_semantics.py" `
      ".\tests\test_phase144_6_r5_15m_evidence_contributions.py" `
      ".\tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15U focused tests failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15U integration audit"
    Write-Host ("=" * 78)
    python (Join-Path $scriptDir "audit_phase144_6_r5_15u.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15U audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
