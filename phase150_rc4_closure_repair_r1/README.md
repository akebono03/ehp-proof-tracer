# Phase 150 / RC4 Closure Repair R1

Minimal production repair for the cross-group reason/presentation boundary.

Changed production function:

- `toda_group_proof_narrative_reasons.py`
- `build_toda_group_proof_narrative_reason_sidecar`

The classifiers are unchanged. The builder now accepts a reason only when all
premise steps and the conclusion step are present in the current presentation.

Added test:

- `tests/test_phase150_rc4_closure_reason_visibility.py`

The test verifies that the recursive internal `pi_6^3` conclusion inside
`pi_10^4` does not import hidden reason premises, while the visible final-group
reasons for `pi_6^3` and `pi_8^5` remain intact.

The runner performs focused regressions and a representative closure audit.
Repository-wide tests remain deferred until the end of Phase 150.
