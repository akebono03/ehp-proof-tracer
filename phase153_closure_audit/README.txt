Phase 153 Closure Audit
=======================

Purpose
-------
Read-only closure audit for Phase 153 Reference handling.

Production changes
------------------
None.

Population
----------
112 groups:
- n = 2..15
- k = 0..7
- Narrative depth = 2

Checks
------
For every rendered group Narrative:

1. Reference header numbering is contiguous: R1, R2, ..., Rn.
2. Reference numbers are unique.
3. Reference titles are not duplicated.
4. The root theorem's LiteratureReference is not listed as an external
   Reference.
5. Every body [Rk] marker resolves to a displayed Reference.
6. For marker-bearing routes, every displayed Reference is actually used in
   the body.
7. Generic/reference-only routes are allowed to have no textual [Rk] markers,
   because Phase 153-R11 attributes them structurally by used ProofStep.
8. All 112 groups render without exceptions.

This package also reruns the focused Phase 153 R8-R12 tests.

Boundary
--------
This package does NOT run the full pytest suite.

If the audit passes, the next step is the Phase 153 final full pytest.

Narrative prose cleanup, including punctuation normalization to "," and ".",
belongs to Phase 154 and is intentionally excluded here.
