Phase157-R20 repair53-r3b — pi15 Reference number audit

Purpose
-------
Determine whether the legacy pi_15^8 dedicated renderer's hard-coded [R1]
marker still points to Proposition 4.4 after repair53-r3 split the graph
Reference identities into Proposition 4.4 and Proposition 5.15.

Production code changes
-----------------------
None.

pytest
------
Not run.

Audit output
------------
- all [R#] markers present in the dedicated proof body;
- graph Reference entry numbering;
- fixed-boundary Reference entry numbering;
- statement lines by Reference number;
- entries retained by body-use filtering;
- marker lines after filtering.

Expected diagnostic
-------------------
If Proposition 4.4 is no longer Reference number 1 while the dedicated body
still contains only [R1], body-use filtering will retain the wrong Reference
and discard Proposition 4.4.

Next step
---------
Repair only the specialized Reference connector / marker remapping if this is
confirmed. Do not alter the fixed-statement attribution logic, which already
passes its focused tests.
