Phase 161-R4-R5 repair12
Fixed component source resolution

Root cause
==========
Repair11 selected an internal premise of the aggregate Proposition 5.1 step.
That premise is upstream of the aggregate, so the nearest visible consumer is
still the general higher-eta component.

The graph is:

  aggregate Proposition 5.1
    -> fixed higher-eta component step
    -> pi_4^3 specialization

The Reference section displays the fixed higher-eta component, so linkage must
also start from that fixed component step itself.

Repair
======
Modify:

  _phase154_r5_reference_source_steps_by_number()

For every selected aggregate Reference step:

1. Determine the displayed aggregate component with the existing:
     _phase153_r6_reference_aggregate_component()
2. Search the presentation for steps whose conclusion equals that component.
3. Keep only FIXED_STATEMENT steps with:
     boundary.reference_locator == entry.reference.locator
     boundary.component_key is not None
4. If exactly one such fixed component step exists, use it as the effective
   linkage source.
5. Do not re-add the replaced aggregate step through entry.proof_steps.
6. Otherwise fall back to the original behavior.

No Proposition 5.1 or pi_4^2 specific production condition is added.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py
  - _phase154_r5_reference_source_steps_by_number()

New:
- tests/test_phase161_r4_r5_repair12_fixed_component_source_resolution.py

Imports
=======
No production import changes.

Expected output
===============
Reference:
- R1 Toda (5.2), general form
- R2 Proposition 5.1, general higher-eta form

Body:
- [R2]より, pi_4^3 = Z/2{eta_3}.
- [R1] applied at i=4.
- eta_3 -> eta_2 eta_3.
- pi_4^2 = Z/2{eta_2^2}.
- QED

Full pytest is not run until Phase161 ends.
