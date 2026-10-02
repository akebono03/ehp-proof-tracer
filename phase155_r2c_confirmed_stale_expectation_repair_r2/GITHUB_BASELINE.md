# GitHub baseline — Phase 155-R2C-r2

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Rechecked before R2C-r2:

- `tests/test_phase132_6_group_proof_narrative_renderer.py`
- `tests/test_phase153_r12_root_reference_exclusion.py`
- `tests/test_phase154_r6_1_repair3_ascii_period_policy.py`
- `tests/test_phase154_r6_2_ascii_comma_normalization.py`

The Phase 154 current-contract test for pi11_4 explicitly expects:

- `[R1]を用いる.`
- `[R2]より, $\nu_{4}$ の分解写像は同型写像である.`

R2C-r2 therefore repairs the stale Phase 153 expectation to that semantic
form rather than forcing both references into the same compact marker shape.

For the Phase 132 depth-1 test, R2C-r2 narrows punctuation checking to the
discourse leads instead of asserting that no Japanese period exists anywhere
in that older presentation route.
