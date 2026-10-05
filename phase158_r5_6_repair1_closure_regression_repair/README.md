# Phase 158-R5-6 repair1 — closure regression repair

## Purpose

This repair addresses the failures found by the Phase 158-R5-6 focused regression.

## Production change

`toda_group_proof_narrative_equation_numbering.py`

The numbering pass previously added a transition target to the numbering set even when that equation was never referenced later. After the R5 generic ordering changes, this could leave a terminal equation such as `(3)` numbered without any later `(3) より` reference.

The repair removes that target-only numbering path. An equation receives a number only when it is actually used as a visible source by a later transition.

## Test repairs

`tests/test_phase157_r5_r10_reference_proof_boundary_qed.py`

The Phase 158 public Narrative contract now normalizes the terminal QED marker to the literal `□`. The older Phase 157 expectations for `$\square$` are updated accordingly, including the Web rendered-line expectation.

`tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py`

Two old expectations are superseded by the Phase 158 single generic public Narrative route:

- The π10⁴ test no longer freezes the older prose fragment `以上で得た群構造`; it checks the current final-target narrative contract in both public Markdown and Web text.
- The π8⁵ test no longer requires the old dedicated-route introduction. It checks the current public Narrative shell and target, and explicitly rejects that stale introduction.

## Scope

No unrelated refactoring is included.

Repository-wide pytest is intentionally not run here. It remains reserved for the final Phase 158 closure.

## Completion condition

1. Direct repaired-contract tests pass.
2. The complete R5 focused regression passes.
3. `git diff --check` passes.
