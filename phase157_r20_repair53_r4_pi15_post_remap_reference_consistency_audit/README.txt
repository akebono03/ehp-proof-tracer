Phase157-R20 repair53-r4
pi_15^8 post-remap Reference consistency audit

Purpose
-------
After repair53-r3c and r3d2/r3d3, re-audit the final pi_15^8
Reference state without changing production code or tests.

The audit prints:

- graph Reference entries
- graph statement lines
- entries after root exclusion / current Reference boundary
- available Phase157 literature-boundary API names
- final public Reference entries
- final public body [R#] markers and marker lines
- complete public proof body
- candidate inconsistencies
- targeted Proposition 4.4 / Proposition 5.15 checks

Hard failures
-------------
The audit exits non-zero only for clear structural defects:

- body marker points to no public Reference
- duplicate public Reference number
- duplicate public Reference locator
- Proposition 4.4 is not present exactly once
- Proposition 4.4 is present but its marker is not used in the body

Candidate-only findings
-----------------------
These are printed for review but do not automatically fail the audit:

- public Reference without body marker
- non-root graph locator omitted from public
- public locator absent from non-root graph

Those can be legitimate after body-use filtering, so they require
interpretation before any production repair is made.

Changes
-------
Production code: none
Tests: none
Documents: none

pytest
------
Not run.

Repository-wide pytest remains reserved for the end of Phase 157.
