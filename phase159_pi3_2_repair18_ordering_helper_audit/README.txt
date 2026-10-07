Phase 159 pi3_2 repair18 ordering-helper audit

Purpose
-------
Inspect the local-only repair18 ordering helper after repair22.

No production code or test is changed.

The audit prints:
- _phase159_order_public_unique_preimage_definition_premises() source
- current repair18 test constants
- actual public paragraphs after repair22
- which expected constants are stale/missing

Repository-wide pytest is intentionally not run.
