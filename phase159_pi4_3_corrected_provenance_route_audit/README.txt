Phase 159 — pi_4^3 corrected provenance route audit
====================================================

Purpose
-------
Correct one false-negative risk in the previous audit and determine the
actual proof route used by the current pi_4^3 group-result provenance.

The previous audit treated pi_4^5=0 as though it were a Relation.
In the current repository it is a TodaPrimaryGroupZeroStatement.

This audit checks:

1. whether pi_4^5=0 is actually a direct premise of E-surjectivity;
2. whether Delta(iota_5)=+/-2eta_2 is in current pi_4^3 provenance;
3. which premises the current Im(Delta) step actually uses;
4. whether the existing direct bridge rule can derive
   Delta(iota_5)=+/-2eta_2 from the current ancestry;
5. whether the current Im(Delta) rule can consume a reduced candidate
   set containing that direct Delta statement.

No production files or existing tests are modified.

Focused pytest
--------------
tests/test_phase50_pi4_3_exactness_bridge.py
tests/test_phase52_delta_direct_bridge.py
tests/test_phase55_prop51_integration.py

Repository-wide pytest is not run.
