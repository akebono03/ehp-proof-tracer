$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $repoRoot

try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15P apply"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "apply_phase144_6_r5_15p.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15P apply failed."
    }

    Copy-Item `
      (Join-Path $scriptDir "tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py") `
      ".\tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py" `
      -Force

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15P focused tests"
    Write-Host ("=" * 78)

    pytest -q `
      ".\tests\test_phase144_6_r5_15m_evidence_contributions.py" `
      ".\tests\test_phase144_6_r5_15p_evidence_contribution_vocabulary.py" `
      ".\tests\test_phase141_5_narrative_blocks_semantics.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15P focused tests failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15P audit"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "audit_phase144_6_r5_15p.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15P audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
