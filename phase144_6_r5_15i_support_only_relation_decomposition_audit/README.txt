Phase 144-6-R5-15I
====================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-15H showed that evidence-function semantics are promising, but SUPPORT_ONLY
still contains:
- 13 visible direct selected-owner edges
- 4 hidden direct selected-owner edges
- 409 visible nested edges
- 5238 hidden nested edges

R5-15I decomposes SUPPORT_ONLY by the relation between premise and consumer.

Priority
--------
1. Direct selected-owner SUPPORT_ONLY
2. Visible nested SUPPORT_ONLY
3. Hidden nested SUPPORT_ONLY

Candidate relations
-------------------
CLAIM_INPUT
  Direct input to a selected final-claim Argument conclusion.

PROVIDER_INPUT
  Direct input to a selected typed/integration provider.

REFERENCE_INPUT
  Support consumed by a reference block.

DEFINITION_INPUT
  Support consumed by a definition block.

STRUCTURAL_INPUT
  Support consumed by group/order/membership structure.

COMPUTATION_INPUT
  Support consumed by a calculation.

PRECONDITION_INPUT
  Support consumed by a precondition.

MAP_INPUT
  Support consumed by a map-property statement.

AGGREGATE_INPUT
  Support involving an existing generic aggregate statement.

RESIDUAL_SUPPORT
  Remaining SUPPORT_ONLY relation not explained above.

Constraints
-----------
No n/k-specific visibility rule.
No inference-rule-name parsing.
No production visibility changes.
No pytest because production code is unchanged.
