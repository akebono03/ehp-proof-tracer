Phase157-R20 repair52 — Residual route ownership audit

Purpose
-------
Determine the exact local owners of the six repair51 findings and the
pi_4^3 eta_3 = eta_3 display.

Production code changes
-----------------------
None.

pytest
------
Not run.

Targets
-------
- pi_4^3
  - root statement repeated twice
  - visible eta_3 = eta_3 ownership
  - legacy recursive renderer route
- pi_8^5
  - isolated "を得る." paragraph
  - dedicated Phase134-9 renderer ownership
- pi_15^8
  - isolated "である." / "を得る." paragraphs
  - dedicated Phase134-24 renderer ownership

Why audit before repair
-----------------------
repair51 established that these are the only residual display findings among
112 groups. They belong to older output routes rather than the new repair42-48
generic ordering rules.

This audit verifies the local cumulative repository before deciding whether
repair53 should:
- add a generic final prose normalization shared by all routes;
- or minimally repair the old dedicated/legacy route assembly.

No production code is modified.
