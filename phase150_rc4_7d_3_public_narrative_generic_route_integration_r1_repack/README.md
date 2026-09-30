# Phase 150 RC4-7D-3 Public Narrative Generic Route Integration R1

## Changed targets

Production:

- `toda_group_proof_narrative_renderer.py`
  - add `_is_phase150_rc4_generic_route_target`
  - change the complete `render_toda_group_proof_narrative_markdown`

Tests:

- add `tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py`

## Import changes

None.

## New helper insertion position

Immediately before `render_toda_group_proof_narrative_markdown`.

## Scope

At depth 2 or greater, only these RC4 targets are newly connected to the
existing generic multi-Argument contribution/reason route:

- `pi_10^4`
- `pi_12^5`
- `pi_16^9`

Existing routes are preserved for `pi_6^3`, `pi_8^5`, `pi_15^8`, and depth
0/1 RC4 targets.

No Web template, Flask endpoint, reason classification, Argument ownership,
transition role, or contribution ordering is changed.

## Completion criteria

- six focused route tests pass;
- RC4-7D reason regressions pass;
- related Web/Narrative regressions pass;
- Web snapshots visibly contain the generic reason prose;
- repository-wide pytest is not run.

## Phase boundary

Reason selection/ownership quality remains the next RC4-7D task after route
integration is confirmed. RC5 semantic naming and RC6 formatting remain out
of scope.
