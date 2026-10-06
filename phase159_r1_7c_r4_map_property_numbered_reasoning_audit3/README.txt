Phase 159 R1-7c R4 map-property numbered-reasoning audit3

Purpose
-------
Audit2 found three unnumbered same-map injective+surjective pairs:

- pi_9^3:
  Delta: pi_9^5 -> pi_7^2
- pi_10^3:
  Delta: pi_10^5 -> pi_8^2
- pi_11^6:
  H: pi_7^3 -> pi_7^5

Only pi_11^6 already has a visible isomorphism conclusion.

Before changing public formatting, audit3 checks whether each pair has an
actual isomorphism ProofStep in either:
- raw presentation;
- semantic-closure presentation.

This is required because the renderer must not infer or invent a semantic
isomorphism merely from two visible prose lines.

The current repository contains a generic Hopf injective+surjective implies
isomorphism rule, but no corresponding generic Delta isomorphism rule was
found during GitHub inspection.

Scope
-----
Audit only.

Production code changes: none.
Test code changes: none.
No full pytest.
