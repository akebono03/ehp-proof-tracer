# Phase 144-6 R25-9A — pi_5^3 Suppression Isolated Repair

## Changed files

- `toda_group_proof_narrative_argument_multi_renderer.py`
  - `_toda_group_proof_narrative_argument_frontier_hidden_step_ids()`
- `tests/test_phase144_6_r25_9a_pi5_suppression.py`
  - new focused regression tests

## Production change

The current HEAD protects the premises of every direct premise for every
Narrative Argument. That makes second-level support facts visible even when
they are not part of the intended Narrative frontier.

R25-9A restores the earlier general rule:

- every Argument preserves its direct premises and transition endpoints;
- only `ESTABLISH_DEFINITION` preserves one additional premise-support layer.

This is not a pi_5^3 text special case. It is a role-based frontier rule.

## Scope boundary

R25-9A does not change:

- `toda_upstream_bootstrap.py`;
- replay depth selection;
- semantic-sidecar construction;
- the missing nu-prime definition at CLI depth 2.

That separate issue belongs to R25-9B.

## Focused tests

The runner checks:

- the new R25-9A role boundary;
- Phase 144-6 R4 supporting-fact suppression;
- definition frontier and transition chains;
- Phase 143 direct-premise extraction;
- Phase 144-6 R5-15U evidence integration.

The full suite is intentionally deferred until the end of Phase 144-6.
