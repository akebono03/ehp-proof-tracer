Phase 146-4 Renderer Quality Contract Audit

Purpose
-------
Inspect output-quality properties of the existing generic multi-argument
renderer across the six representative groups.

This is not a production implementation.

Checks
------
- selected contributions
- contribution insertion availability
- non-detached versus detached contribution insertion
- selected contribution renderer fallback count
- whether contribution insertion changes the base output

Why this follows Phase 146-3
----------------------------
Phase 146-3 showed that all six groups satisfy basic semantic readiness:
purpose subjects, conclusion steps, purpose sentences, and a unique
group-structure argument are all available. Those properties therefore
cannot safely distinguish generic-route readiness.

Production changes
------------------
None.

Existing test changes
---------------------
None.

Boundary
--------
Do not replace the pi6 route gate until a genuine renderer-quality contract
is identified. Raw target coordinates, theorem names, argument counts, and
coverage ratios are explicitly out of scope as capability predicates.
