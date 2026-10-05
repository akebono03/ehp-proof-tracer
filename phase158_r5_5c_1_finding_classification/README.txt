Phase 158-R5-5c-1 — finding classification

Purpose
-------
Classify only the five equation-chain findings reported by Phase 158-R5-5c.
This phase is audit-only. It does not change production code or existing tests.

Findings in scope
-----------------
- pi_7^3:  (1) と (2) より,
- pi_10^5: (1) より,
- pi_11^5: (1) より,
- pi_12^6: (1) より,
- pi_12^6: (2) より,

Classification contract
-----------------------
REAL_ORDERING_DEFECT
  A referenced numbered source is missing or is not earlier than the connector.
  This is a confirmed public ordering defect.

CONNECTOR_TARGET_NOT_TAGGED
  All numbered sources are earlier and a mathematical target immediately follows,
  but the target has no tag. Tag absence alone is not a production ordering bug.

AUDIT_HARNESS_FALSE_POSITIVE
  All numbered sources are earlier and the immediately following target is tagged.
  The original R5-5c finding is therefore a harness false positive.

TARGET_VISIBILITY_SUPPRESSION
  The connector is absent, is terminal, or is followed by non-mathematical visible
  content. This remains undecided until a separate pipeline inspection proves whether
  suppression is correct or incorrect.

Outputs
-------
audit_output/summary.txt
audit_output/classification.csv
audit_output/finding_context.txt
audit_output/exceptions.csv

Boundary
--------
- No production code changes.
- No existing test changes.
- No repository-wide pytest.
- No repair is attempted in this phase.
- A later repair phase is created only if classification proves a real production defect.
