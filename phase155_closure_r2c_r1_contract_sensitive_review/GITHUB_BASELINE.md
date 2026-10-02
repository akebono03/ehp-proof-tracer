# GitHub baseline — Phase 155 Closure-R2C-R1

Repository: `akebono03/ehp-proof-tracer`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before R2C:
- tests/test_phase95_top_level_calculation_orchestration.py
- tests/test_phase97_single_found_calculation_to_report_api.py
- tests/test_phase97_not_found_multiple_results_top_level_handling.py
- tests/test_phase98_actual_use_facade_validation.py
- tests/test_phase98_representative_convenience_validation.py
- tests/test_phase153_r2_public_reference_semantic_fact.py
- tests/test_phase153_r3_10_public_reference_connection_repair.py
- tests/test_phase153_r3_11_reference_body_ownership_repair.py
- tests/test_phase153_r3_4_reference_statement_rendering_connection.py
- tests/test_phase153_r3_5_reference_body_duplicate_suppression.py
- toda_calculation_report.py
- toda_calculation_report_result.py

Key observation:
The three extreme tests assert candidate ordering/provenance contracts while
constructing large historical integration data. Their first repair should
replace fixtures, not weaken the contract.

No Phase156 functionality is implemented.
