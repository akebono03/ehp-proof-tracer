Phase 159-R1-6b repair2

Scope
-----
Test-only repair.

Reason
------
R1-6b intentionally changed map-property equation numbering from:

  $H: ...\tag{1}$ は単射.

to:

  $H: ... \text{ は単射}. \tag{1}$

The R1-4 regression test still asserted the old contract.

Production changes
------------------
None.

Test change
-----------
Update only:

  test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically()

The revised test also asserts that the old tag placement no longer appears.

Full pytest
-----------
Not run.
