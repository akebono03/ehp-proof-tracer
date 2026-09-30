$ErrorActionPreference="Stop"
Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Repair R4"
Write-Host "Order-calculation semantic closure + precise test repair"
Write-Host "=============================================================="
$env:PYTHONPATH=(Get-Location).Path
$env:PYTHONIOENCODING="utf-8"

Write-Host "`nA. Applying R4..."
python ".\phase148_rc2_5_repair_r4_order_calculation_closure\apply_phase148_rc2_5_repair_r4.py"

Write-Host "`nB. Syntax preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_semantics.py" `
  ".\tests\test_phase148_rc2_5_semantic_closure_scope.py"

Write-Host "`nC. Focused regression..."
$tests=@(
"tests/test_phase132_6_group_proof_narrative_renderer.py",
"tests/test_phase132_7_group_proof_cli_modes.py",
"tests/test_phase133_7_group_proof_narrative_labels.py",
"tests/test_phase134_3_pi6_3_numbered_narrative.py",
"tests/test_phase134_5_pi6_3_reference_fact_split.py",
"tests/test_phase134_6_pi6_3_mathbook_narrative.py",
"tests/test_phase134_7_pi6_3_final_narrative.py",
"tests/test_phase134_9_pi6_3_snapshot.py",
"tests/test_phase136_1_pi6_3_narrative_prose.py",
"tests/test_phase136_2_pi6_3_narrative_structure.py",
"tests/test_phase143_47_multi_argument_shared_contribution_dedup.py",
"tests/test_phase143_49_dependency_label_narrative_policy.py",
"tests/test_phase143_50_generic_statement_prose_renderer.py",
"tests/test_phase143_63a_r_exactness_repair.py",
"tests/test_phase143_63a_residual_fallback_provenance.py",
"tests/test_phase144_6_pi6_generic_production_route.py",
"tests/test_phase144_6_public_route_cutover.py",
"tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py",
"tests/test_phase148_rc2_3_exactness_exposure.py",
"tests/test_phase148_rc2_4_repair_r2.py",
"tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py",
"tests/test_phase148_rc2_5_semantic_closure_scope.py"
)
$existing=@()
foreach($t in $tests){if(Test-Path $t){$existing+=$t}else{Write-Host "SKIP optional missing test: $t"}}
pytest -q @existing
if($LASTEXITCODE -ne 0){throw "R4 focused regression failed. Do NOT run repository-wide pytest."}

Write-Host "`n=============================================================="
Write-Host "R4 focused regression: PASS"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "Send this output back for final Phase 148 whole-suite run."
Write-Host "=============================================================="
Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING
