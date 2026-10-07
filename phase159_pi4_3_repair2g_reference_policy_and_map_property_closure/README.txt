Phase 159 — pi_4^3 repair2g
================================

Goal
----
Apply the same Reference policy already chosen for pi_3^2:

  [R1] (5.1)
  [R2] Proposition 5.1

for the pi_4^3 depth-2 public Narrative.

EHP exactness is NOT a Reference. This is a project-wide policy.

Mathematical boundary
---------------------
(5.1) is the foundational fixed statement

  pi_i^1 = 0  (i > 1),
  pi_i^n = 0  (i < n),
  pi_n^n = Z{iota_n}.

For pi_4^3 it supplies the specializations pi_4^5=0 and
pi_5^5=Z{iota_5}, but these are not split into separate Reference entries.

Proposition 5.1 supplies the low-dimensional eta facts used by the proof,
including pi_3^2=Z{eta_2} and Delta(iota_5)=+/-2eta_2.

Implementation scope
--------------------
Changed production files:

1. toda_proof_dependency.py
   - import section
   - classify_toda_proof_step_role()
   - TodaDeltaImageFreeCyclicStatement and
     TodaSuspensionKernelFreeCyclicStatement become MAP_PROPERTY.

2. toda_literature_statement_boundary.py
   - add fixed (5.1) component
   - map (5.1) foundational rule names
   - classify Phase159 direct Proposition 5.1 Delta rule as fixed
   - classify the Phase50 pi_3^2 Proposition 5.1 source as fixed

3. toda_upstream_bootstrap.py
   - add _toda_fixed_reference_metadata_rule()
   - _build_phase49_result(): keep GIVEN rules, attach (5.1) metadata
   - _build_phase50_result(): keep GIVEN rules, attach (5.1) and
     Proposition 5.1 metadata
   - existing Phase159 repair1 direct Delta route remains unchanged

4. toda_group_proof_narrative_contribution_renderer.py
   - _phase157_r20_canonical_fixed_reference_line()
   - render (5.1) as one general fixed statement, not separate concrete facts

5. toda_group_proof_narrative_references.py
   - filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary()
   - foundational (5.1) is ordered before other fixed references

Added test:
- tests/test_phase159_pi4_3_repair2g_reference_policy.py

Not changed
-----------
- EHP exactness semantics
- EHP exactness Reference policy
- proof search
- group APIs
- stable-range logic
- pi_6^3 special handling
- repository-wide tests

Expected public Reference
-------------------------
pi_3^2:
  [R1] (5.1)

pi_4^3:
  [R1] (5.1)
  [R2] Proposition 5.1

No Proposition 4.2 / EHP exactness entry may appear in the Reference section.

Important
---------
This package assumes Phase159 pi_4^3 repair1/1a/1b/1c is already applied.
It checks for the direct Proposition 5.1 Delta(iota_5) route and stops
instead of silently reverting to the old Whitehead-specific route.

This repair intentionally does NOT claim pi_4^3 proof-body completion.
It establishes the correct Reference boundary and exposes the map-property
ancestry needed for the next proof-body repair.

Repository-wide pytest is NOT run.
