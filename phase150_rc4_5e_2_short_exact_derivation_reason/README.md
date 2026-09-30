# Phase 150 / RC4-5E-2

Minimal implementation of typed reason prose for the derived short exact
sequence.

Production changes:
- `toda_group_proof_generic_narrative_renderer.py`
- `toda_group_proof_narrative_argument_body_renderer.py`

Added focused test:
- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`

The existing `_generic_short_exact_sequence_latex(...)` already requires a
typed exactness window, a matching injective first map, and a matching
surjective second map. RC4-5E-2 reuses exactly that contract.

A derived short exact sequence is a synthetic presentation contribution, not a
`ProofStep`. This change therefore does not manufacture a fake conclusion step
and does not broaden `TodaGroupProofNarrativeReason`.

Repository-wide tests remain deferred until the end of Phase 150.
