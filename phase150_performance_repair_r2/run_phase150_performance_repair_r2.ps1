$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Performance Repair R2"
Write-Host "Cache repeated Phase 144-6 R5-19..25 audit construction"
Write-Host "Production changes: none"
Write-Host "Audit builder changes: none"
Write-Host "Mathematical assertions changed: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

$Tests = @(
  ".\tests\test_phase144_6_r5_19_proof_chain_narrative_integration.py",
  ".\tests\test_phase144_6_r5_20_pi6_3_proof_chain_generic_parity.py",
  ".\tests\test_phase144_6_r5_21_missing_7_facts_generic_provider_audit.py",
  ".\tests\test_phase144_6_r5_22_missing_4_facts_statement_structure_audit.py",
  ".\tests\test_phase144_6_r5_23_missing_7_facts_generic_visibility_path_audit.py",
  ".\tests\test_phase144_6_r5_24_generic_visibility_policy_correction_design_audit.py",
  ".\tests\test_phase144_6_r5_25_multi_argument_suppression_selective_frontier_relevance_audit.py"
)

try {
    Write-Host ""
    Write-Host "A. Applying minimal test-only performance repair..."
    python "$ScriptRoot\apply_phase150_performance_repair_r2.py"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Syntax preflight..."
    foreach ($Test in $Tests) {
        python -m py_compile $Test
        if ($LASTEXITCODE -ne 0) {
            exit $LASTEXITCODE
        }
    }
    Write-Host "Syntax preflight: PASS"

    Write-Host ""
    Write-Host "C. Focused R5-19..25 regression with durations..."
    $Started = Get-Date

    python -m pytest @Tests -q `
      --durations=50 `
      --durations-min=0.0 `
      2>&1 |
      Tee-Object -FilePath ".\phase150_performance_repair_r2_focused.txt"

    $PytestExit = $LASTEXITCODE
    $Elapsed = (Get-Date) - $Started

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host ("Focused elapsed: {0:N2} seconds" -f $Elapsed.TotalSeconds)
    Write-Host "pytest exit code: $PytestExit"
    Write-Host "Full regression: NOT run"
    Write-Host "Output: .\phase150_performance_repair_r2_focused.txt"
    Write-Host "=============================================================="

    exit $PytestExit
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
