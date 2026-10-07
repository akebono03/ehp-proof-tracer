Phase 159 pi3_2 numbered pipeline audit

Purpose
-------
Inspect where the current public pipeline loses the Phase 159 R1-7c
numbered map-property contract.

No production code or tests are changed.

The current contract is:
  $H: ...\tag{1}$ は単射.
  $H: ...\tag{2}$ は全射.
  (1), (2) より, $H: ...$ は同型.

This audit prints the public renderer source, relevant helper sources,
intermediate pipeline outputs, and final output.
