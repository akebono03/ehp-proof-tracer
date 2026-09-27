$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
    $env:PYTHONPATH = (Get-Location).Path

    Write-Host ("=" * 78)
    Write-Host "Phase 144-5-R1: focused-test escape correction"
    Write-Host ("=" * 78)

    python ".\phase144_5_r1_test_fix\apply_phase144_5_r1.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-5-R1 patch failed."
    }

    Write-Host ""
    Write-Host ("=" * 78)
    Write-Host "Focused regression tests only (NOT full pytest)"
    Write-Host ("=" * 78)

    pytest -q `
      ".\tests\test_phase144_5_generic_definition_order_equations.py" `
      ".\tests\test_phase143_49_dependency_label_narrative_policy.py" `
      ".\tests\test_phase142_3_generic_proof_text.py" `
      ".\tests\test_phase143_2_generic_short_exact_sequence.py"

    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-5-R1 focused tests failed."
    }

    Write-Host ""
    Write-Host ("=" * 78)
    Write-Host "pi_6^3 generic Narrative preview"
    Write-Host ("=" * 78)

    python ".\phase144_5_generic_definition_order_equations\preview_phase144_5.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 144-5 preview failed."
    }
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Pop-Location
}
