Phase 144-6-R5-41
Contribution topological-order determinism audit

Production changes: none.

Added:
- audit_phase144_6_r5_41.py
- tests/test_phase144_6_r5_41_contribution_topological_order_determinism_audit.py

Purpose:
For the 190 Phase-40 selected explanatory contributions, build an owner-Argument
partial order from ProofStep reachability and measure whether topological order
is unique. For non-unique DAGs, record ready-set width and the number of steps
that would require a stable tie-break.

The diagnostic stable key is used only to make the audit reproducible. It is
not introduced as a production Narrative ordering rule.

The pi_6^3 five-contribution Argument is explicitly required to form a unique
topological chain.

No production code is changed. Run only focused Phase-40 and Phase-41 tests.
