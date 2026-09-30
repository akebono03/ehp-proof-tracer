Phase 148 RC2-4 Repair R1 — Exposure-path Audit

Purpose
-------
The previous RC2-4 audit verified exposure only through exactness method
components. The actual Web Narrative for pi_6^3 still contains many exactness
statements.

This package performs a reverse trace from every TodaProp42ExactnessStatement
that is actually visible in the final pi_6^3 Narrative.

Production changes
------------------
None.

Existing repository test changes
--------------------------------
None.

Audit-only test
---------------
tests/test_phase148_rc2_4_repair_r1_exposure_path_audit.py

For each exactness statement the diagnostic reports:
- source block index
- source block role
- whether the exactness rendering is visible in the final Narrative
- membership in each Argument's method evidence
- membership in each Argument's local body
- whether it is a direct derivation premise
- whether it is a direct-premise support step
- RC2 exposure classification, if any

The summary separately counts:
- visible exactness statements
- visible exactness statements outside EXACTNESS-role blocks
- visible exactness statements with no RC2 exposure classification

This is an audit only. It intentionally does not modify:
- exactness exposure policy
- proof graph
- provenance
- Argument ordering
- Narrative ordering

No repository-wide pytest is run.
