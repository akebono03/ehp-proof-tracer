Phase 148 RC2-1 Repair R2

Purpose
-------
Correct an audit-harness-only comparison error in Repair R1.

Observed failure
----------------
Repair R1 used:

    assert primary is components[0]

The Phase 147 ownership API rebuilds the exactness components internally.
Therefore the returned primary component is structurally equal to the
component built by the audit harness, but it is not required to be the same
Python object.

The existing Phase 147 regression test already uses value equality for this
boundary.

Repair
------
Exactly two assertions in:

phase148_rc2_1_repair_r1/test_phase148_rc2_1_repair_r1.py

are changed from:

    primary is components[0]

to:

    primary == components[0]

No production code is changed.
No existing repository test is changed.
No exposure policy is implemented in RC2-1.

Run
---
From the repository root:

powershell -ExecutionPolicy Bypass `
  -File ".\phase148_rc2_1_repair_r2\run_phase148_rc2_1_repair_r2.ps1"

Completion
----------
Focused tests must pass and the exposure audit must complete.

Repository-wide pytest is intentionally not run here because RC2-1 is not
the end of Phase 148.

Next boundary
-------------
RC2-2: design the minimal general exactness-evidence exposure rule.

RC3 Narrative ordering remains out of scope.
