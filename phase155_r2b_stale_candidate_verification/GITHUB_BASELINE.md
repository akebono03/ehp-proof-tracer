# GitHub baseline for Phase 155-R2B

Confirmed before implementation against:

- Repository: `akebono03/ehp-proof-tracer`
- Branch: `main`
- Observed commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Current-contract evidence inspected:

- `tests/test_phase154_r6_1_repair3_ascii_period_policy.py`
- `tests/test_phase154_r6_2_ascii_comma_normalization.py`
- `tests/test_phase154_r4_semantic_duplication_transition_refinement.py`
- `tests/test_phase153_r10_used_reference_filtering.py`
- `tests/test_phase153_r12_root_reference_exclusion.py`
- `tests/test_phase144_6_pi6_generic_production_route.py`
- `README.md`
- `docs/development_log.md`

Relevant current contract:

- Public Japanese Narrative prose uses ASCII `, ` and `.`.
- Internal statement/type fallback names must not leak into public prose.
- Repeated semantic reason prose is deduplicated.
- Reference display is governed by used-reference filtering, root exclusion,
  renumbering, granularity, and reuse rules.
- Historical presentation expectations have previously required maintenance
  after later generalization phases.

R2B deliberately verifies candidates by focused execution rather than by
treating old Phase numbers or string patterns as proof of staleness.
