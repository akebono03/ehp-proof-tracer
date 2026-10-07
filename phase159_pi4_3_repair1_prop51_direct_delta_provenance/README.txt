Phase 159 — pi_4^3 repair 1
Proposition 5.1 direct Delta-image provenance
=============================================

Scope
-----
This repair changes only the mathematical provenance used to derive Im(Delta)
for the current pi_4^3 proof.

It does not repair Narrative Argument ownership or public prose suppression.

General rule added
------------------
If

  G = Z{g}

and

  Delta(g) = +/- x,

then

  Im(Delta) = Z{x}.

This rule is not hard-coded to pi_4^3.

pi_4^3 bootstrap change
-----------------------
The Phase 50 bootstrap receives the fixed literature statement

  Delta(iota_5) = +/- 2 eta_2

with Toda Proposition 5.1 attribution.

The new generic rule is evaluated before the existing Whitehead-specific
pi_4^3 Delta-image rule, so the derived Im(Delta) proof step owns the direct
Proposition 5.1 statement as its premise.

Existing Whitehead-specific rules are retained for API/test compatibility.

Files
-----
Added:
  toda_delta_image_rules.py

Changed:
  toda_upstream_bootstrap.py
    imports
    _build_phase50_result()

Added:
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py

Focused verification
--------------------
tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py
tests/test_phase50_pi4_3_exactness_bridge.py
tests/test_phase50_pi4_3_finite_cyclic.py
tests/test_phase52_delta_direct_bridge.py

Repository-wide pytest is intentionally not run.

Completion condition
--------------------
1. The generic direct Delta-image rule derives the expected image.
2. It rejects a mismatched free generator.
3. The pi_4^3 Im(Delta) step directly depends on the Proposition 5.1
   Delta(iota_5)=+/-2eta_2 statement.
4. The final pi_4^3 result remains unchanged.
5. Focused regression passes.

Next boundary
-------------
After this repair, re-audit the depth=2 Narrative ownership/suppression path.
Do not change Narrative ownership in this repair.
