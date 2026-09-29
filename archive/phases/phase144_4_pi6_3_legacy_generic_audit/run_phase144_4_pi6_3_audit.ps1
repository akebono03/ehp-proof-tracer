$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
    $env:PYTHONPATH = (Get-Location).Path

    Write-Host ("=" * 78)
    Write-Host "Phase 144-4: pi_6^3 legacy vs generic residual-difference audit"
    Write-Host ("=" * 78)

    python ".\phase144_4_pi6_3_legacy_generic_audit\audit_phase144_4_pi6_3.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-4 audit failed."
    }

    Write-Host ""
    Write-Host ("=" * 78)
    Write-Host "Focused regression tests only (NOT full pytest)"
    Write-Host ("=" * 78)

    pytest -q `
      ".\tests\test_phase134_9_pi6_3_snapshot.py" `
      ".\tests\test_phase142_2_generic_narrative_renderer.py" `
      ".\tests\test_phase142_3_generic_proof_text.py" `
      ".\tests\test_phase143_2_generic_short_exact_sequence.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Focused regression tests failed."
    }

    Write-Host ""
    Write-Host "Phase 144-4 audit completed."
    Write-Host "Review:"
    Write-Host "  .\phase144_4_pi6_3_legacy_generic_audit\output\phase144_4_audit_report.md"
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Pop-Location
}
