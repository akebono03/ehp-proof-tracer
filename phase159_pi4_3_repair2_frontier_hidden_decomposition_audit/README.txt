Phase 159 — pi_4^3 repair 2
Frontier-hidden decomposition audit
===================================

Purpose
-------
The previous audit established that the pi_4^3 support chain reaches the
renderer local body, but most of it disappears before final markdown.

This audit identifies every step hidden by:

  _toda_group_proof_narrative_argument_frontier_hidden_step_ids()

and compares body rendering with frontier hiding enabled versus disabled.

Production code changes:
  none

Existing test changes:
  none

This audit does not repair:
- depth=2 semantic closure,
- Proposition 5.1 reference exposure,
- renderer prose.

Repository-wide pytest is not run.
