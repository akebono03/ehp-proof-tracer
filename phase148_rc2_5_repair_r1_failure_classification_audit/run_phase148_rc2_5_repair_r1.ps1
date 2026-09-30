$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Repair R1 - 23-failure classification audit"
Write-Host "Production changes: none"
Write-Host "Existing tests changed: none"
Write-Host "=============================================================="
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "A. Syntax preflight..."
python -m py_compile ".\phase148_rc2_5_repair_r1_failure_classification_audit\audit_phase148_rc2_5_repair_r1.py"

Write-Host ""
Write-Host "B. Reproducing the 23 known failures (failure is expected here)..."
pytest -q `
  "tests/test_phase132_6_group_proof_narrative_renderer.py::test_phase132_6_depth_zero_does_not_invent_premises" `
  "tests/test_phase132_7_group_proof_cli_modes.py::test_phase132_7_group_proof_depth_zero_is_shared_across_modes[narrative-# Group proof narrative]" `
  "tests/test_phase133_7_group_proof_narrative_labels.py::test_phase144_6_supersedes_legacy_pi6_3_narrative_contract" `
  "tests/test_phase134_3_pi6_3_numbered_narrative.py::test_phase144_6_supersedes_legacy_pi6_3_narrative_contract" `
  "tests/test_phase134_5_pi6_3_reference_fact_split.py::test_phase144_6_supersedes_legacy_pi6_3_narrative_contract" `
  "tests/test_phase134_6_pi6_3_mathbook_narrative.py::test_phase144_6_supersedes_legacy_pi6_3_narrative_contract" `
  "tests/test_phase134_7_pi6_3_final_narrative.py::test_phase144_6_supersedes_legacy_pi6_3_narrative_contract" `
  "tests/test_phase134_9_pi6_3_snapshot.py::test_phase144_6_supersedes_legacy_pi6_3_narrative_contract" `
  "tests/test_phase136_1_pi6_3_narrative_prose.py::test_phase144_6_supersedes_legacy_pi6_3_narrative_contract" `
  "tests/test_phase136_2_pi6_3_narrative_structure.py::test_phase144_6_supersedes_legacy_pi6_3_narrative_contract" `
  "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py::test_phase143_47_pi8_5_suppresses_shared_exactness_contributions" `
  "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py::test_phase143_47_pi16_9_suppresses_shared_definition_evidence" `
  "tests/test_phase143_49_dependency_label_narrative_policy.py::test_phase143_49_pi8_5_narrative_hides_dependency_labels" `
  "tests/test_phase143_49_dependency_label_narrative_policy.py::test_phase143_49_pi16_9_narrative_hides_dependency_labels" `
  "tests/test_phase143_50_generic_statement_prose_renderer.py::test_phase143_50_pi8_5_renders_exactness_and_definition_in_japanese" `
  "tests/test_phase143_50_generic_statement_prose_renderer.py::test_phase143_50_pi16_9_renders_exactness_in_japanese" `
  "tests/test_phase143_63a_r_exactness_repair.py::test_phase143_63a_r_pi8_5_exactness_is_single_japanese_sentence" `
  "tests/test_phase143_63a_r_exactness_repair.py::test_phase143_63a_r_pi16_9_exactness_is_single_japanese_sentence" `
  "tests/test_phase143_63a_residual_fallback_provenance.py::test_phase143_63a_pi6_3_exactness_fallback_is_japanese" `
  "tests/test_phase144_6_pi6_generic_production_route.py::test_phase144_6_public_pi6_3_narrative_equals_generic_argument_renderer" `
  "tests/test_phase144_6_public_route_cutover.py::test_phase144_6_public_pi6_3_equals_contribution_renderer" `
  "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py::test_phase144_6_r25_9b_adds_only_required_definition_endpoint" `
  "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py::test_phase144_6_r25_9b_depth2_narrative_has_definition_without_pi5_3"
Write-Host "Known-failure reproduction exit code: $LASTEXITCODE"

Write-Host ""
Write-Host "C. Running classification diagnostic..."
python ".\phase148_rc2_5_repair_r1_failure_classification_audit\audit_phase148_rc2_5_repair_r1.py" |
  Tee-Object -FilePath ".\phase148_rc2_5_repair_r1_failure_classification_audit\rc2_5_repair_r1_output.txt"
if ($LASTEXITCODE -ne 0) {
  throw "Classification diagnostic failed."
}

Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING
Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Repair R1 audit: COMPLETE"
Write-Host "Production changes: none."
Write-Host "Existing tests changed: none."
Write-Host "Repository-wide pytest: not run."
Write-Host "Next: minimal production/test repair from the classification."
Write-Host "=============================================================="
