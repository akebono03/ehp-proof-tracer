Phase 161-R4-R5
pi_4^3 Proposition 5.1 Reference linkage

Problem
=======
The pi_4^2 public proof uses:

  pi_4^3 = Z/2{eta_3}

as a concrete premise, but the Reference section currently contains only Toda
(5.2).

The concrete pi_4^3 step has no literature reference of its own. Its literature
basis is the general higher-eta group component of Toda Proposition 5.1:

  pi_{n+1}^n = Z/2{eta_n}, n >= 3.

Design
======
Do not patch the renderer with a pi_4^2-specific string rule.

Instead, add a proof-graph linkage step between:
- the independently derived concrete pi_4^3 relation; and
- the fixed Toda Proposition 5.1 aggregate.

The linkage step itself has no LiteratureReference. It only records provenance.

The existing generic Reference machinery can then expose Proposition 5.1 and
link it to the visible concrete pi_4^3 premise.

Files
=====
Modified:
- toda_prop56_zero_bootstrap.py

New:
- tests/test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py

Production imports
==================
The `proof` import adds:
- InferenceRule

Existing API
============
`_build_pi4_2_step` keeps its existing two required positional arguments.

A new optional argument is added:
- prop51_step: ProofStep | None = None

Therefore existing callers remain valid.

Changed/new production functions
================================
- new `_build_pi4_3_prop51_specialization_link_step`
- changed `_build_pi4_2_step`
- changed `build_toda_prop56_zero_argument_step`

Full replacement units are written to `output/`.

Completion criteria
===================
- Proposition 5.1 appears in the pi_4^2 Reference section.
- its general higher-eta relation is shown in Reference.
- Toda (5.2) remains in Reference.
- pi_4^3 remains concrete in the proof body.
- the pi_4^3 paragraph carries the Proposition 5.1 Reference marker.
- pi_4^2 conclusion and QED remain.
- existing focused R4 and provenance regressions pass.

The full test suite is not run until the end of Phase161.
