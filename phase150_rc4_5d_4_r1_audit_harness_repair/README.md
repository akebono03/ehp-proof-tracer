# Phase 150 / RC4-5D-4-R1

Repairs only the RC4-5D-4 audit harness.

## What was wrong in RC4-5D-4

1. The audit treated absence of the plain equality line as if there were no
   ordering gap. The actual Narrative passes the calculation chain through
   generic equation numbering, so the equality appears as a tagged line.
2. The runner named Phase 149 ordering tests that do not exist in the current
   repository.

## Current repository facts used by this audit

- `toda_group_proof_narrative_argument_multi_renderer.py` calls
  `number_toda_group_proof_narrative_equations(...)`.
- `toda_group_proof_narrative_equation_numbering.py` converts the generic
  calculation chain into numbered equations and dependency references.
- The current Phase 149 regression is
  `tests/test_phase149_rc3_4_cross_group_ordering.py`.
- The current equation-numbering regression is
  `tests/test_phase144_5_generic_definition_order_equations.py`.

## Boundary

No production files or existing tests are changed. This audit does not move
the `(1),(2) -> (3)` calculation chain. It only determines ownership of the
ordering pressure so RC4 does not prematurely implement RC6 equation-numbering
work.

Repository-wide tests remain deferred until the end of Phase 150.
