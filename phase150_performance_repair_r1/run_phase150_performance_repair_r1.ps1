$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Performance Repair R1"
Write-Host "Minimal Phase 144-6 audit recomputation repair"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying minimal repair..."
    python "$ScriptRoot\apply_phase150_performance_repair_r1.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host ""
    Write-Host "B. Syntax preflight..."
    python -m py_compile `
      ".\audit_phase144_6_r5_39.py" `
      ".\tests\test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host ""
    Write-Host "C. Focused Phase 144-6 R5-37 through R5-41 regression + timing..."
    $Started = Get-Date

    python -m pytest `
      ".\tests\test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py" `
      ".\tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py" `
      ".\tests\test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py" `
      ".\tests\test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py" `
      ".\tests\test_phase144_6_r5_41_contribution_topological_order_determinism_audit.py" `
      -q `
      --durations=50 `
      --durations-min=0.0 `
      2>&1 |
      Tee-Object -FilePath ".\phase150_performance_repair_r1_focused.txt"

    $PytestExit = $LASTEXITCODE
    $Elapsed = (Get-Date) - $Started

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 150 Performance Repair R1 result"
    Write-Host ("Focused elapsed: {0:N2} seconds" -f $Elapsed.TotalSeconds)
    Write-Host "pytest exit code: $PytestExit"
    Write-Host "output: .\phase150_performance_repair_r1_focused.txt"
    Write-Host "Full regression: NOT run"
    Write-Host "=============================================================="

    exit $PytestExit
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
