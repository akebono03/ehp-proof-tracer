$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $repoRoot

try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15P-R1 apply"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "apply_phase144_6_r5_15p_r1.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15P-R1 apply failed."
    }

    Copy-Item `
      (Join-Path $scriptDir "tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py") `
      ".\tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py" `
      -Force

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15P-R1 syntax/import preflight"
    Write-Host ("=" * 78)

    python -m py_compile ".\toda_group_proof_narrative_evidence_contributions.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15P-R1 syntax preflight failed."
    }

    python -c "from toda_group_proof_narrative_evidence_contributions import TodaGroupProofNarrativeEvidenceContribution as E; assert E.ESTABLISH_EXACTNESS.value == 'establish_exactness'; assert E.ESTABLISH_DEFINITION.value == 'establish_definition'; assert E.ESTABLISH_MEMBERSHIP.value == 'establish_membership'"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15P-R1 import preflight failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15P-R1 focused tests"
    Write-Host ("=" * 78)

    pytest -q `
      ".\tests\test_phase144_6_r5_15m_evidence_contributions.py" `
      ".\tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py" `
      ".\tests\test_phase141_5_narrative_blocks_semantics.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15P-R1 focused tests failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15P-R1 audit"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "audit_phase144_6_r5_15p.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15P-R1 audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
