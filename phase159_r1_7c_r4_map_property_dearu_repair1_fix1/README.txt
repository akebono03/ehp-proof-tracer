Phase 159 R1-7c R4 map-property "である" repair1 fix1

Cause
-----
The repair1 production normalization worked. Three of four focused tests passed.

The only failure was a stale Reference-prefix expectation:

  expected: [R1] より,
  current public contract: [R1]より,

Current GitHub outputs and prior Phase157/158 public contracts use the latter.

Change
------
Production code changes: none.

Update only:

  tests/test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py

Specifically, the pi_11^6 concise map-property test now expects:

  [R1]より, $H: ...$ は単射.

No semantic, renderer, Reference-selection, or punctuation behavior changes.

No full pytest.
