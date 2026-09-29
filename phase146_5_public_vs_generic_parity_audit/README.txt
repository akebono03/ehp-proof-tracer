Phase 146-5 Public-vs-Generic Parity Audit

Purpose
-------
Compare the current public Narrative output with the generic
multi-argument-with-contributions renderer for the six representative groups.

This is an audit only.

Measurements
------------
- exact output parity
- character counts
- non-empty line counts
- line-sequence similarity
- changed diff hunks
- math-containing lines found only in public output
- math-containing lines found only in generic output

Interpretation
--------------
Exact parity is already expected for pi_6^3 by the current public-cutover
tests. For other groups, differences show where historical public routes or
fallback rendering still diverge from the generic semantic pipeline.

Character counts and similarity ratios are diagnostic only. They must not
become routing predicates.

Production changes
------------------
None.

Existing test changes
---------------------
None.

Boundary
--------
The next implementation target must be selected from a concrete semantic
difference found by this audit. Do not replace the pi_6^3 route gate with a
target-shaped proxy condition.
