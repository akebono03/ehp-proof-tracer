Phase 144-6-R5-14
===================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
Measure the proof depth implied by the R5-13 provider model.

Seeds
-----
ATOMIC:
  Definition/Order Narrative Argument conclusions that establish final
  generator/order components.

TRANSPORT:
  Typed structural statements recognized in R5-13.

INTEGRATION_DIRECT_PREMISE:
  Root direct premises that structurally participate in integration,
  including group-structure relations and typed aggregate/decomposition
  statements.

Method
------
For each seed, follow actual provenance edges from parent step to premise step
and compute the unrestricted premise closure. Compare:

  provider seed depth
  unrestricted provider closure depth
  full provenance depth

This audit intentionally does NOT insert a semantic stopping boundary.

Why
---
If unrestricted provider closure reaches full proof depth, then provider
selection is no longer the main problem. The remaining problem is to define
where a Narrative provider is allowed to treat a typed theorem/lemma or
Argument as an explanatory boundary.

Targets
-------
pi_6^3
pi_8^5
pi_10^4
pi_12^5
pi_15^8
pi_16^9

Important checks
----------------
- pi_6^3 must not be declared solved just because its provider seed depth is 3.
- pi_10^4 and pi_15^8 must not incorrectly collapse to depth 0.
- If their integration direct premises are selected, the audit measures the
  real proof closure below those premises.
