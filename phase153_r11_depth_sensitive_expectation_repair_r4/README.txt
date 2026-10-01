Phase 153-R11 Depth-sensitive Expectation Repair R4
================================================

Purpose
-------
Repair only the stale depth-2 R11 test expectation.

Why R3 failed
-------------
R3 tried to match the full function body with a regex.
The local test file differed enough that the pattern matched zero times.

R4 repair
---------
R4 finds the target test by its exact function name and replaces everything
from that function declaration up to the next top-level def.

Production changes
------------------
None.

Changed test
------------
tests/test_phase153_r11_generic_reference_attribution_filtering.py

Expected depth-2 behavior
-------------------------
- Reference section exists.
- (5.3) remains.
- Proposition 5.3 remains.
- Proposition 5.6 self-reference does not remain.
- Proposition 4.4 / Proposition 5.1 are not required at depth 2.

Full pytest remains deferred until the end of Phase 153.

Punctuation normalization remains deferred.
Final prose style should use "," and "." instead of "、" and "。".
