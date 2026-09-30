# Phase 149 RC3-3 Minimal Implementation

This package applies the minimal RC3 ordering change.

## Scope

- Keeps Phase 148 RC2 exactness ownership and exposure classification unchanged.
- Does not change the proof graph, exactness component construction, argument ordering, or step-transition model.
- Defers visible `OWNED_PRIMARY` exactness display contributions until immediately before the owning Argument's conclusion block.
- Falls back to the existing location if an owning conclusion is not available.
- Adds focused tests for the `pi_6^3` ordering symptom and RC2 visibility invariants.

## Files changed

- `toda_group_proof_narrative_argument_body_renderer.py`

## Test added

- `tests/test_phase149_rc3_3_minimal_ordering.py`

## Phase boundary

This package does not perform the RC3-4 six-group ordering audit and does not run the repository-wide test suite. Those remain later Phase 149 work.
