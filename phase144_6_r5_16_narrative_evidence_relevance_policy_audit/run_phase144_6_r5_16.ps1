$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $repoRoot

try {
    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-16 preflight"
    Write-Host ("=" * 78)

    pytest -q `
      ".\tests\test_phase144_6_r5_15u_r1_evidence_integration.py" `
      ".\tests\test_phase144_6_r5_15t_aggregate_semantics.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-16 preflight failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-16 audit import preflight"
    Write-Host ("=" * 78)

    python -m py_compile `
      (Join-Path $scriptDir "audit_phase144_6_r5_16.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-16 audit import preflight failed."
    }

    Write-Host ("=" * 78)
    Write-Host "Phase 144-6-R5-16 Narrative evidence relevance policy audit"
    Write-Host ("=" * 78)

    python (Join-Path $scriptDir "audit_phase144_6_r5_16.py")

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-6-R5-16 audit failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
