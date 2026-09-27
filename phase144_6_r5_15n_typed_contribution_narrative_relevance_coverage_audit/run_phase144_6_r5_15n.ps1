$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$env:PYTHONPATH = $repoRoot

try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15N preflight"
    Write-Host ("=" * 78)

    if (-not (Test-Path ".\toda_group_proof_narrative_evidence_contributions.py")) {
        throw "15M production prototype file is missing. Apply the successful 15M package first."
    }

    pytest -q `
      ".\tests\test_phase144_6_r5_15m_evidence_contributions.py"

    if ($LASTEXITCODE -ne 0) {
        throw "15M focused prototype tests failed. Stop before 15N audit."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-15N coverage audit"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "audit_phase144_6_r5_15n.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-15N audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
