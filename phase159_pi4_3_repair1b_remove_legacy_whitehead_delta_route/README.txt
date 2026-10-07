Phase 159 — pi_4^3 repair 1b
Remove legacy Whitehead Delta route
===================================

Reason
------
Repair 1a removed the legacy Whitehead-specific Im(Delta) rule from
_build_phase50_result(), but the generic direct Delta-image rule still
saw two Delta(iota_5) statements:

  Delta(iota_5) = +/-2 eta_2

and

  Delta(iota_5) = +/-[iota_2, iota_2].

Therefore it correctly derived two different image statements.

Scope
-----
Only toda_upstream_bootstrap.py is changed.

Removed from its imports:
  toda_delta_iota5_whitehead_square_inference_rule

Removed from _build_phase50_result().rules:
  toda_delta_iota5_whitehead_square_inference_rule()

The rule implementation remains in toda_rules.py. Its standalone API and
existing focused tests remain unchanged.

The pi_3^2 Whitehead-square rule is intentionally retained.

Expected Phase 50 route
-----------------------
  pi_5^5 = Z{iota_5}
  Delta(iota_5) = +/-2 eta_2        [Toda Proposition 5.1]
  => Im(Delta) = Z{2 eta_2}
  => ker(E) = Z{2 eta_2}

No Narrative ownership or rendering changes are made.

Focused verification
--------------------
tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py
tests/test_phase50_pi4_3_exactness_bridge.py
tests/test_phase50_pi4_3_finite_cyclic.py
tests/test_phase52_delta_direct_bridge.py

Completion condition
--------------------
1. Phase 50 contains exactly one direct Delta(iota_5) statement.
2. Phase 50 contains no legacy Delta(iota_5)=+/-[iota_2,iota_2] step.
3. Phase 50 contains exactly one Im(Delta) step.
4. That Im(Delta) step is derived by the generic direct rule.
5. Its Delta premise is attributed to Toda Proposition 5.1.
6. Final pi_4^3 ancestry contains no legacy Whitehead Delta route.
7. Focused tests pass.

Repository-wide pytest is not run.

Next boundary
-------------
After repair 1b passes, repair 1 is mathematically/provenance complete.
The next task is a focused Narrative ownership/depth-2 re-audit.
