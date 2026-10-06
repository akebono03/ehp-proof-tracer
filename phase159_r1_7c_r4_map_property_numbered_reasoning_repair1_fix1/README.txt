Phase 159 R1-7c R4 numbered map-property reasoning repair1 fix1

Cause
-----
The numbered-reasoning production repair passed its own focused tests.

The only failure came from the previous map-property prose regression, which
still expected an unnumbered pi_11^6 Hopf injective/surjective display.

Old expectation:
  [R1]より, $H: ...$ は単射.
  $H: ...$ は全射.

Current intended public contract:
  [R1]より, $H: ...\tag{1}$ は単射.
  $H: ...\tag{2}$ は全射.

Change
------
Production code changes: none.

Update only:
  tests/test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py

The test continues to verify concise prose while accepting the new numbering
contract.

No semantic changes.
No Reference changes.
No full pytest.
