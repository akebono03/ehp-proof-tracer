$ErrorActionPreference="Stop"
$P=Split-Path -Parent $MyInvocation.MyCommand.Path
$R=(Get-Location).Path
$T=Join-Path $R "tests"
$M=Join-Path $T "__init__.py"
$C=$false
$OP=$env:PYTHONPATH
$OE=$env:PYTHONIOENCODING
try {
 if(-not(Test-Path $M)){New-Item -ItemType File -Path $M -Force|Out-Null;$C=$true}
 $env:PYTHONPATH="$R;$T";$env:PYTHONIOENCODING="utf-8"
 Write-Host "Phase 144 Final Historical Snapshot Repair R3"
 Write-Host "Production renderer changes: none"
 python (Join-Path $P "apply_phase144_final_historical_snapshot_repair_r3.py")
 if($LASTEXITCODE-ne 0){throw "patch failed"}
 python -m pytest -q `
 "tests/test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py" `
 "tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py" `
 "tests/test_phase144_6_r5_41_contribution_topological_order_determinism_audit.py" `
 "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py" `
 "tests/test_phase144_6_r5_43_1.py" `
 "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py" `
 "tests/test_phase144_6_r5_43_11a_insertion_failure_classification_audit.py" `
 "tests/test_phase144_6_r5_43_11b_detached_argument_boundary_audit.py" `
 "tests/test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py" `
 "tests/test_phase144_6_r5_43_11c_r2_argument_participation_guard.py" `
 "tests/test_phase144_6_r5_43_11d_final_completion_audit.py" `
 "tests/test_phase144_6_r5_43_3.py" `
 "tests/test_phase144_6_r5_43_generic_renderer_contribution_connection.py" `
 "tests/test_phase144_6_r5_43_r2_recursive_repr_repair.py"
 if($LASTEXITCODE-ne 0){throw "focused tests failed; do not rerun whole suite"}
 git status --short
 Write-Host "R3 focused tests: PASS"
 Write-Host "Do NOT rerun the whole repository suite."
} finally {
 if($null-eq$OP){Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue}else{$env:PYTHONPATH=$OP}
 if($null-eq$OE){Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue}else{$env:PYTHONIOENCODING=$OE}
 if($C-and(Test-Path $M)){Remove-Item $M -Force}
}
