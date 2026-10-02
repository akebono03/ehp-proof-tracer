# GitHub baseline — Phase 155-R3-1

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Current GitHub tests inspected before the R3-1 audit:

- `tests/test_phase154_r6_1_repair3_ascii_period_policy.py`
- `tests/test_phase154_r6_2_ascii_comma_normalization.py`
- `tests/test_phase153_r10_used_reference_filtering.py`
- `tests/test_phase153_r12_root_reference_exclusion.py`
- `tests/test_phase150_rc4_7b_production_repair.py`
- `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`
- `tests/test_phase144_6_pi6_generic_production_route.py`
- `tests/test_phase143_53b_r_conclusion_aware_connector.py`
- `README.md`

Key observation:

Later Phase 154 punctuation tests may overlap with older local presentation
tests, but they also provide broader representative-group invariants. String
overlap alone is therefore not sufficient evidence that an older test is
superseded.

R3-1 uses conservative static evidence only and authorizes no deletion.
