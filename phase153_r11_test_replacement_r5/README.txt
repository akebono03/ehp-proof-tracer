Phase 153-R11 Test Replacement R5
=====================================

Purpose
-------
Stop doing partial replacements on the locally modified R11 test file.

Production changes
------------------
None.

Changed
-------
The entire newly added R11 test file is replaced:

tests/test_phase153_r11_generic_reference_attribution_filtering.py

This avoids depending on any intermediate local state left by earlier repair
attempts.

Depth-2 expectations
--------------------
- Reference section exists.
- Proposition 5.6 self-reference is absent.
- (5.3) remains.
- Proposition 5.3 remains.

Proposition 4.4 and Proposition 5.1 are not required by this depth-2 test.
Existing depth-3 tests continue to cover the deeper Reference scope.

Boundary
--------
Full pytest remains deferred until the end of Phase 153.
Punctuation normalization remains deferred.
Final prose style should use "," and "." instead of "、" and "。".
