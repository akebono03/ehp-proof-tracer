Phase 159 — pi_4^3 repair 1a
Remove duplicate legacy Delta-image route
=========================================

Reason
------
Repair 1 added the generic direct rule

  G = Z{g}, Delta(g) = +/-x
  => Im(Delta) = Z{x}

and connected the Proposition 5.1 statement

  Delta(iota_5) = +/-2 eta_2.

However, _build_phase50_result() still ran the legacy
Whitehead-specific pi_4^3 Im(Delta) rule.

Both rules derived the same TodaDeltaImageFreeCyclicStatement, so the
inference result contained two distinct ProofStep objects with the same
conclusion.

Scope
-----
Only toda_upstream_bootstrap.py is changed.

Removed from the import list:
  toda_pi4_3_delta_image_free_cyclic_inference_rule

Removed from _build_phase50_result() rules:
  toda_pi4_3_delta_image_free_cyclic_inference_rule()

The legacy rule implementation remains in toda_rules.py and is not deleted.
Existing API/tests that use it directly remain valid.

No Narrative ownership or rendering changes are included.

Focused verification
--------------------
tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py
tests/test_phase50_pi4_3_exactness_bridge.py
tests/test_phase50_pi4_3_finite_cyclic.py
tests/test_phase52_delta_direct_bridge.py

Completion condition
--------------------
- Exactly one Im(Delta) ProofStep exists in Phase 50.
- It directly owns the Proposition 5.1 Delta(iota_5)=+/-2eta_2 premise.
- The final pi_4^3 ancestry contains exactly one Im(Delta) step.
- Focused tests pass.

Repository-wide pytest is not run.
