Phase 161-R4-R5 repair8 active-helper audit

Purpose
=======
The source-step audit proved:

- Proposition 5.1 R3 source step is correct.
- Its unique visible consumer is exactly pi_4^3.
- The proof graph is correct.

Repair6 logic should therefore relocate the marker, but the final public output
still does not.

This audit verifies the runtime function itself.

It prints:
- the source file and first line of the active contribution helper
- the source file and first line of the helper imported by the outer renderer
- whether both names point to the same function object
- the complete active helper source
- the direct R3 consumer result
- a synthetic body before and after a direct helper call
- the full public render

No production or tests are changed.

Interpretation
==============
If the direct synthetic call does not move R3:
  the defect is inside the helper implementation.

If the direct call moves R3 but the full public render does not:
  a later pipeline stage reintroduces or rewrites the Proposition 5.1 line.

Full pytest is not run.
