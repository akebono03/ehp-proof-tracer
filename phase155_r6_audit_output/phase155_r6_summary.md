# Phase 155-R6 — pytest collection / runtime audit

## Collection

- files: 837
- batches: 21
- total collected cases observed: 10421
- collection elapsed seconds (sum of batch observations): 379.93

Collected cases mapped to R5 lanes:
- canonical_routine: 8972
- historical_compatibility: 65
- audit_only: 288
- performance_heavy_integration: 29
- residual_retained: 664

## Bounded runtime probe

- selected probes: 12
- per-probe timeout: 60s
- canonical_routine: probes=3, pass=3, fail=0, timeout=0, max_pass=1.85s
- historical_compatibility: probes=2, pass=2, fail=0, timeout=0, max_pass=2.65s
- audit_only: probes=2, pass=2, fail=0, timeout=0, max_pass=4.40s
- performance_heavy_integration: probes=3, pass=3, fail=0, timeout=0, max_pass=26.55s
- residual_retained: probes=2, pass=2, fail=0, timeout=0, max_pass=1.37s

Slowest bounded probes:
- 26.55s PASS performance_heavy_integration tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py::test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered
- 7.51s PASS performance_heavy_integration tests/test_phase150_rc4_7a_cross_group_reference_normalization.py::test_phase150_rc4_7a_pi16_9_numbers_normalized_references
- 4.40s PASS audit_only tests/test_phase108_12_end_to_end_cli_smoke_closure_audit.py::test_phase108_12_execute_nu_prime_candidate_1_returns_result_and_proof_end_to_end
- 3.76s PASS performance_heavy_integration tests/test_phase144_6_r5_17c_cross_group_generic_proof_chain.py::test_phase144_6_r5_17c_applies_unchanged_extractor_to_all_five_groups
- 3.14s PASS audit_only tests/test_phase96_final_proof_report_audit.py::test_phase96_12_unknown_statement_fallback_is_explicit_and_safe
- 2.65s PASS historical_compatibility tests/test_phase72_probe.py::test_phase72_probe_output_marks_hand_authored_presentation
- 1.85s PASS canonical_routine tests/test_toda_rules.py::test_toda_statements_are_outside_generic_equality_scope
- 1.71s PASS canonical_routine tests/test_algebra.py::test_abelian_group_structure_z
- 1.56s PASS historical_compatibility tests/test_phase100_12c2_minimal_cli_integration.py::test_phase100_12c2_cli_not_found_is_explicit_and_nonzero
- 1.39s PASS canonical_routine tests/test_phase57_lemma45_two_iota3.py::test_phase57_2_lemma45_rule_matches_alpha_in_pi_i_s3

## Completion

- collection_batches_have_no_failures: PASS
- runtime_probes_have_no_failures: PASS
- canonical_regression_not_run: PASS
- repository_wide_pytest_not_run: PASS
- checkpoint_resume_enabled: PASS

**Phase 155-R6 audit validated: True**

Canonical regression: NOT run.
Repository-wide pytest: NOT run.

R6 is measurement only. It does not delete tests or change production behavior.
