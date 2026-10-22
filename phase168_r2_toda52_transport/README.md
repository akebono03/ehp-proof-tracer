# Phase 168 R2 — Toda (5.2) typed backward transport

## Scope

This guarded patch adds a single inference route for the first 2-stem group $\pi_4^2$. It uses the **already screened** `Toda52UniversalStatement` and requests the $\pi_4^3$ finite-cyclic relation as a proof subgoal. It does not manufacture either premise and does not import a historical completed proof.

The mathematical specialization is deliberately restricted to $i=4$. Generalization and the next group are left for subsequent work.

## Changes

- `phase168_r2_toda52_transport.py` (new): `_eta2_composition_parts`, `_toda52_rule`, `expand_toda52_finite_cyclic_goal`.
- `phase165_r52_r9_shared_math.py`: entire existing `shared_expansion_provider` function, with two inserted statements immediately after the `expand_finite_cyclic_relation(goal)` call. The installer preserves all existing statements and refuses unknown shapes.
- `tests/test_phase168_r2_toda52_transport.py`: 3 focused tests.
- `run.ps1`: guarded installation, focused pytest, active search check.

## Exit criteria

The active search must return `COMPLETE`, with no open goals, verified proof steps, valid source links, and a correct conclusion. The package does not claim these criteria in advance: if the screened $\pi_4^3$ relation is still unavailable, the search remains partial. Full pytest is deferred to the end of Phase 168.
