Phase 153-R11 Depth-sensitive Expectation Repair R3
================================================

Purpose
-------
Repair only the stale depth-2 test expectation.

Production changes
------------------
None.

Changed test
------------
tests/test_phase153_r11_generic_reference_attribution_filtering.py

New expectation
---------------
For pi_6^3 at max_depth=2:
- the Reference section exists;
- (5.3) remains;
- Proposition 5.3 remains;
- Proposition 5.6, the theorem currently being proved, is not listed as an
  external Reference.

The test no longer requires Proposition 4.4 or Proposition 5.1, because those
are deeper-scope expectations covered separately by existing depth-3 tests.

Boundary
--------
Full pytest remains deferred until the end of Phase 153.

Punctuation normalization remains deferred.
Final prose style should use "," and "." instead of "、" and "。".
