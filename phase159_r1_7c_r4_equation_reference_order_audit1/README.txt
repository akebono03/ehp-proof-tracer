Phase 159 R1-7c R4 equation-reference order audit1

Purpose
-------
The numbered-reasoning closure audit succeeded formally, but the current
pi_5^3 public Narrative exposes a proof-order defect:

  (1), (2) より, E は同型.

appears before the lines defining (1) and (2).

This audit searches public proof bodies for equation-number references of the
form:

  (n) より,
  (n), (m) より,
  (n) と (m) より,

and verifies that every referenced \tag{n} line appears earlier in the proof.

A reference is classified as forward when:
- the referenced tag exists only later; or
- the referenced tag cannot be found in the current proof body.

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
