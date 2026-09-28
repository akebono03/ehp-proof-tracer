# Phase 144-6 R25-9A-R1 — Relocated Hidden-Step Repair

## Changed files

- `toda_group_proof_narrative_argument_multi_renderer.py`
  - keeps the R25-9A role-based frontier repair already applied
- `toda_group_proof_narrative_argument_body_renderer.py`
  - `render_toda_group_proof_narrative_argument_body_markdown()`
- `tests/test_phase144_6_r25_9a_pi5_suppression.py`
  - retained from R25-9A
- `tests/test_phase144_6_r25_9a_r1_relocation_hidden.py`
  - new focused regression test

## Root cause

R25-9A correctly marks second-level support steps as hidden for non-definition
Arguments. However, `render_toda_group_proof_narrative_argument_body_markdown()`
has a second display route:

`direct_derivation_support_steps -> relocated_direct_premises -> insertion`

The normal block display route applies `context_hidden_step_ids`, but the
relocation selection did not. A hidden support step could therefore be
reinserted immediately before an Argument conclusion.

Historical Phase 143-75AP R13 documentation explicitly states that
`context_hidden_step_ids still applies` when provenance/derivation premises are
preserved.

## Production repair

The relocated-premise filter now also requires that a premise is not in
`context_hidden_step_ids`.

This is a generic rendering invariant. It contains no pi_5^3, pi_6^3, n/k, or
Toda-family special case.

## Scope boundary

R25-9A-R1 does not change:

- upstream proof construction;
- replay depth selection;
- semantic-sidecar construction;
- the missing nu-prime definition at CLI depth 2.

That remains the separate R25-9B problem.

## Focused tests

The runner checks:

- a direct unit regression for hidden relocated premises;
- R25-9A role-based frontier tests;
- Phase 144-6 R4 supporting-fact suppression and transition chains;
- Phase 143 direct-premise extraction;
- Phase 144-6 R5-15U evidence integration.

The full suite is intentionally deferred until the end of Phase 144-6.
