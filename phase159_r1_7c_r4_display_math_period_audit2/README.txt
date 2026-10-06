Phase 159 R1-7c R4 display-math period audit2

Purpose
-------
Refine the display-math punctuation audit after audit1 produced five false
positives.

Current numbered display contract
---------------------------------
A numbered mathematical sentence may end as:

  sentence. \qquad (n)

The period belongs to the mathematical sentence and therefore appears before
the equation number.

This matches the current desired prose form such as:

  H は単射。(1)

Audit2 therefore accepts both:
- an ordinary display-math line ending in ".";
- a numbered line matching ". \qquad (n)".

Only display-math blocks satisfying neither form are reported as true
missing-period candidates.

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
