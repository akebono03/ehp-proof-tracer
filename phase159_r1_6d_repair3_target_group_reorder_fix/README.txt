Phase 159-R1-6d repair3

Purpose
-------
Fix the repair2 target-group reordering condition.

Cause
-----
Repair2 required the individual target-group Relation step itself to carry the
Toda (5.1) locator. The public Reference linkage can be correct even when that
specific Relation step does not directly carry the locator.

Fix
---
Use the target group from TodaHopfInvariantSurjectiveStatement, render that
group, and locate the existing public line:

  [Rk] より, $<target group> = ...$.

If that line occurs before the numbered surjectivity display, move it to
immediately after the display.

No pi_3^3 string is hard-coded.

Full pytest
-----------
Not run.
