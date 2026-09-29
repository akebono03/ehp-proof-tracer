Phase 144-6-R5-15F
====================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-15E showed:
- CLAIM_EVIDENCE is captured well by the current R4 frontier.
- PROVIDER_EVIDENCE is only partially visible.
- many NESTED_PROOF steps remain visible.

R5-15F classifies nested evidence using existing generic structure.

Candidate actions
-----------------
COLLAPSE_TO_REFERENCE
  The step has structured LiteratureReference provenance.

PROMOTE
  The step already has a reader-facing generic mathematical block role:
  PRECONDITION, DEFINITION, MEMBERSHIP, CALCULATION, EXACTNESS,
  MAP_PROPERTY, ORDER, or GROUP_STRUCTURE.

HIDE
  The step is OTHER and has no structured LiteratureReference.

This is intentionally not yet a production policy. A mathematically meaningful
OTHER statement may reveal a missing semantic role, while a deeply nested
CALCULATION may still be irrelevant to the selected final claim.

The audit therefore reports:
- nested block-role distributions
- candidate action distributions
- R4-visible overlap
- visible nested samples
- hidden PROMOTE samples

No n/k-specific rule is used.
No inference-rule-name parsing is used.
No pytest is run because production code is unchanged.
