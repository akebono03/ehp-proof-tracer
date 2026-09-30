# Phase 150 Performance Repair R2

## Scope

Test-only performance repair for the Phase 144-6 R5-19 through R5-25 audit
tests identified by Phase 150 Performance Diagnostic R3.

Changed files:

- `tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py`
- `tests/test_phase144_6_r5_20_pi6_3_proof_chain_generic_parity.py`
- `tests/test_phase144_6_r5_21_missing_7_facts_generic_provider_audit.py`
- `tests/test_phase144_6_r5_22_missing_4_facts_statement_structure_audit.py`
- `tests/test_phase144_6_r5_23_missing_7_facts_generic_visibility_path_audit.py`
- `tests/test_phase144_6_r5_24_generic_visibility_policy_correction_design_audit.py`
- `tests/test_phase144_6_r5_25_multi_argument_suppression_selective_frontier_relevance_audit.py`

## Change

Repeated no-argument audit builders are cached once per test module.
R5-19 additionally caches `_context(n, k)` and `_render_pair(n, k)` by their
arguments.

Production code, audit builders, public APIs, mathematical assertions, and
Narrative behavior are unchanged.

## Focused test

The runner executes only R5-19 through R5-25 with duration reporting.
It does not run the full regression.

## Completion condition

All focused tests pass and the repeated per-test setup cost is materially
reduced. After that, Phase 150 can proceed to one final full regression.
