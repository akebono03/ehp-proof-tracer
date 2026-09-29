Phase 144-6-R5-10
===================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-9 showed that final-claim-driven selection is selective for pi_6^3 and
pi_8^5, but seven final claim components had no matching Definition/Order
Argument.

R5-10 keeps the final claim components unchanged and audits what actually
provides those claims in the proof provenance.

For each final generator/order component the audit:

1. walks the root-to-premise provenance,
2. finds non-root statements containing the final generator,
3. identifies exact order/group-structure providers when present,
4. otherwise reports the nearest candidate statements,
5. classifies candidates by current Narrative block role and statement type.

Candidate provider categories include:

- DEFINITION
- EXACT_ORDER
- GROUP_STRUCTURE
- CALCULATION_OR_COMPOSITION
- MAP_OR_TRANSPORT
- REFERENCE_THEOREM
- EXACTNESS
- MEMBERSHIP
- OTHER_STATEMENT

This is classification only. No provider-selection policy is implemented.

Representative groups
---------------------
pi_6^3
pi_8^5
pi_10^4
pi_12^5
pi_15^8
pi_16^9
