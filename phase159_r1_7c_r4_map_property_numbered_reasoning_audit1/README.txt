Phase 159 R1-7c R4 map-property numbered-reasoning audit1

Purpose
-------
Audit whether public proof-body map-property reasoning is consistently using
the preferred concise numbered form:

  H は単射. (1)
  H は全射. (2)
  (1), (2) より H は同型.

This audit does not assume that every injective/surjective statement must be
numbered. It inventories:
- numbered injective/surjective public lines;
- unnumbered injective/surjective public lines;
- isomorphism prose lines.

The result will be used to distinguish:
- standalone map-property facts that should remain unnumbered;
- paired injective/surjective arguments that should use numbered reasoning.

Scope
-----
Audit only.

Range:
  n=2..15
  k=0..7
  max_depth=2

This is a reproducible audit sample, not a permanent group-count contract.

Production code changes: none.
Test code changes: none.
No full pytest.
