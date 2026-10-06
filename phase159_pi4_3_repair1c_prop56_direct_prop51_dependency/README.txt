Phase 159 — pi_4^3 repair 1c
Prop56 direct Proposition 5.1 dependency
========================================

Problem
-------
Repair 1b correctly removed the legacy Phase 50 route

  Delta(iota_5) = +/-[iota_2, iota_2]

from _build_phase50_result().

However, toda_prop56_zero_bootstrap._build_prop51_step() still expected that
legacy step and rebuilt

  Delta(iota_5) = +/-2 eta_2

from the Whitehead route.

As a result, the standard production repository could no longer build.

Scope
-----
Changed:
  toda_prop56_zero_bootstrap.py
    _build_prop51_step()

Added:
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py

No imports are changed.
No Narrative renderer/ownership code is changed.

Repair
------
_build_prop51_step() now reuses the direct Proposition 5.1 step already
present in the Phase 50 result:

  Delta(iota_5) = +/-2 eta_2.

It identifies the step by:
- TodaDeltaImageUpToSignStatement
- positive_value is Multiple with coefficient 2
- literature_reference.locator == "Proposition 5.1"

It no longer reconstructs that statement from:
- Delta(iota_5) = +/-[iota_2,iota_2]
- [iota_2,iota_2] = +/-2 eta_2

Boundary
--------
The legacy standalone rules remain available.
This repair only updates the Prop56 bootstrap dependency.

Focused verification
--------------------
- new repair1c tests
- Phase 159 direct Delta provenance tests
- Phase 55 Proposition 5.1 integration tests
- standard production repository build
- previous depth=2 Narrative ownership audit, if its package remains present

Repository-wide pytest is not run.

Completion condition
--------------------
1. _build_prop51_step() builds successfully.
2. Its delta premise is the direct Proposition 5.1 step.
3. The standard production repository builds successfully.
4. Focused tests pass.
5. Then the Narrative ownership audit can proceed.
