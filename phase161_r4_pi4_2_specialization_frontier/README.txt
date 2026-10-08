Phase 161-R4
pi_4^2 proof body specialization / Reference frontier

GitHub audit
============
Audited current repository:
akebono03/ehp-proof-tracer
commit observed:
9242ebb6552a3b6f6c94ee8a10cdfca829c80e10

R3 local state expected:
- recovered contribution renderer
- Phase 161-R3 relink call already applied
- Phase 161-R3 focused tests passing

Problem
=======
The root step

  Toda 5.2 pi_4^2 finite-cyclic transport

is PROOF_INTERNAL and has the same locator `(5.2)` as the fixed literature
statement

  Toda 5.2 eta_2 composition isomorphism

The existing root-reference exclusion compares the locator/reference first.
Because the root boundary is PROOF_INTERNAL, the fixed `(5.2)` entry is
temporarily removed.

That makes the inner Proposition 4.4 ancestry visible during body suppression.
R3 restored `(5.2)` only at the end, so the public Narrative still contained
general-i proof machinery.

R4 changes
==========
1. Root-reference exclusion:
   when the root is PROOF_INTERNAL, retain distinct FIXED_STATEMENT proof steps
   with the same locator.

2. Fixed composition-isomorphism specialization:
   use the semantic map template and the root target group to specialize
   the fixed `(5.2)` statement in the proof body.

For pi_4^2 this gives:

Reference:
  eta_2 o - : pi_i^3 -> pi_i^2 is an isomorphism.

Proof body:
  apply R1 at i=4,
  eta_2 o - : pi_4^3 -> pi_4^2 is an isomorphism,
  and show the generator transport.

3. Proposition 4.4 remains internal to the proof of fixed statement `(5.2)`
   and is not a public Reference for this proof.

Files
=====
Modified:
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_contribution_renderer.py

New test:
- tests/test_phase161_r4_pi4_2_specialization_frontier.py

Updated regression test:
- tests/test_phase161_pi4_2_restored_reference_relink.py
  R3 の `(5.2)` linkage と target/QED を維持し、
  R4 で supersede される Proposition 4.4 public 表示期待を除去する。

Imports
=======
No import changes.

Completion criteria
===================
- `(5.2)` remains in general form in Reference.
- body specializes it to i=4.
- no generic pi_i terms remain in pi_4^2 proof body.
- Proposition 4.4 is not a public Reference/body dependency.
- generator transport is shown.
- target pi_4^2 = Z/2{eta_2^2} and QED remain.
- R3 focused test and Phase161 baseline focused regressions pass.

Phase boundary
==============
Not changed in R4:
- pi_5^3
- pi_6^4 stable base
- stable transport
- Phase157 pi_6^3 stale/known failures
- documentation
- full test suite

The full test suite is reserved for the end of Phase 161.
