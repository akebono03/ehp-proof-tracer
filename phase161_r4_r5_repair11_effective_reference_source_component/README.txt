Phase 161-R4-R5 repair11
Effective Reference source component

Root cause
==========
The final public Reference section displays only the selected component of an
aggregate literature statement, but Reference-body linkage still uses the
aggregate ProofStep as its source.

For Proposition 5.1 this produced:

Displayed Reference:
  pi_{n+1}^n = Z/2{eta_n}

Linkage source:
  Toda Proposition 5.1 finite-dimensional integration

Therefore the nearest visible consumer was the displayed general component
itself, not the concrete pi_4^3 specialization.

Repair
======
Modify:

  _phase154_r5_reference_source_steps_by_number()

For each selected Reference step:

1. Ask the existing aggregate-component selector:
     _phase153_r6_reference_aggregate_component()
2. If no component is selected, keep the original source step.
3. If a component is selected and exactly one premise step has that component
   as its conclusion, use that premise step as the effective linkage source.
4. Otherwise fall back to the original source step.

This keeps Reference display semantics and Reference-body linkage semantics
aligned without adding a Proposition 5.1 or pi_4^2 specific rule.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py
  - _phase154_r5_reference_source_steps_by_number()

New:
- tests/test_phase161_r4_r5_repair11_effective_reference_source_component.py

Imports
=======
No production import changes.

Expected final output
=====================
Reference:
- R1 Toda (5.2), general form
- R2 Proposition 5.1, higher-eta general form

Body:
- [R2]より, pi_4^3 = Z/2{eta_3}.
- [R1]を i=4 に適用すると, eta_2 o -: pi_4^3 -> pi_4^2 は同型.
- eta_3 -> eta_2 eta_3.
- pi_4^2 = Z/2{eta_2^2}.
- QED

Full pytest is not run until Phase161 ends.
