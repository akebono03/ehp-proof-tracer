Phase 144-6-R5-15H
====================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-15G showed that replay depth, owner distance, and Argument/provider boundary
crossing cannot by themselves define Narrative relevance.

R5-15H asks a different question:

  What function does a premise perform for the claim/provider that consumes it?

Candidate evidence functions
----------------------------
ESTABLISH
  Evidence participates in deriving a definition, order, group structure,
  membership, or an existing DERIVATION transition.

COMPUTE
  Evidence participates in an existing calculation-chain transition.

EXACTNESS
  Exactness is structurally involved in the premise-to-parent relation.

TRANSPORT
  A map-property premise is used toward group/order/membership information.

REFERENCE
  The premise has structured LiteratureReference provenance.

SUPPORT_ONLY
  Residual support not explained by the categories above.

Inputs
------
Only existing generic structures are used:
- ProofStep premise edges
- Narrative mathematical block roles
- Narrative transitions
- structured LiteratureReference
- selected final-claim Arguments and typed providers

No n/k-specific visibility rule is used.
No inference-rule-name parsing is used.

This is not a production visibility policy.
No pytest is run because production code is unchanged.
