# Phase 160-R8 Repair 2

Repair only the expected `eta_(n+1)` fixture in the new Phase 160-R8 test.

`toda_eta_family_definition_statement()` accepts only `int` or `ScalarSymbol`. The production function `build_phase59_prop53_step()` therefore does not call that helper with `ScalarSum(n, 1)`. It constructs the symbolic `eta_(n+1)` `HomotopyElement` directly.

This repair makes the focused R8 test use exactly the same construction as production.

No production code is changed. No public Narrative code is changed. No full test suite is run.
