$ErrorActionPreference = "Stop"
$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Copy-Item `
  -Path (Join-Path $scriptDir "toda_group_proof_narrative_evidence_contributions.py") `
  -Destination (Join-Path $repoRoot "toda_group_proof_narrative_evidence_contributions.py") `
  -Force

Copy-Item `
  -Path (Join-Path $scriptDir "tests\test_phase144_6_r5_15m_evidence_contributions.py") `
  -Destination (Join-Path $repoRoot "tests\test_phase144_6_r5_15m_evidence_contributions.py") `
  -Force

$env:PYTHONPATH = $repoRoot
try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15M focused tests"
    Write-Host ("=" * 78)

    pytest -q `
      ".\tests\test_phase144_6_r5_15m_evidence_contributions.py" `
      ".\tests\test_phase141_4_narrative_semantics.py" `
      ".\tests\test_phase141_6_block_audit.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15M focused tests failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15M prototype audit"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "audit_phase144_6_r5_15m.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15M prototype audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
