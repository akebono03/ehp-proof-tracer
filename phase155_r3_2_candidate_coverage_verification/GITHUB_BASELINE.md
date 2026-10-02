# GitHub baseline — Phase 155-R3-2

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Rechecked before R3-2:

- `tests/test_phase154_r6_1_repair3_ascii_period_policy.py`
- `tests/test_phase154_r6_2_ascii_comma_normalization.py`
- `tests/test_phase153_r12_root_reference_exclusion.py`
- `tests/test_phase153_r10_used_reference_filtering.py`
- `tests/test_phase144_6_pi6_generic_production_route.py`
- `tests/test_phase143_53b_r_conclusion_aware_connector.py`
- `tests/test_phase143_55b_conclusion_step_ordering.py`
- `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`

The source review confirms why R3-1 candidates must not be deleted from
assertion overlap alone:

- later punctuation tests can add cross-group invariants,
- older Reference tests can still exercise filtering or root-exclusion logic,
- connector tests can share visible strings while checking different ordering
  relationships,
- a test function may have the same body as another while resolving a local
  helper to different module-level source.

R3-2 therefore verifies direct dependency context as well as test execution.
