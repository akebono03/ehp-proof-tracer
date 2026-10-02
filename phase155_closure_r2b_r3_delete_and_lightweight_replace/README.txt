Phase 155 Closure-R2B-R3 — delete covered historical tests and keep one lightweight invariant

Scope
-----
Uses the completed R2B-R2 outputs:
- delete_candidates.txt (8)
- keep_or_lightweight_replace.txt (1)

Changes
-------
1. Delete exactly eight reviewed historical/covered Phase144 test functions.
2. Replace the one retained heavy cross-group duplicate/order test with a
   representative pi_6^3 proof-step identity / proof-graph ordering test.
3. Remove the original nine nodeids from tests/phase155_audit_only_nodeids.txt.
   The lightweight replacement returns to routine pytest.

Lightweight invariant
---------------------
The replacement does not compare rendered-text occurrence counts.

For pi_6^3 it checks:
- each ordered contribution refers to a distinct proof step;
- if proof step A reaches proof step B in the proof graph, A occurs before B
  in the ordered contribution sequence.

Execution
---------
Only package tooling tests, static deletion verification, and the single
lightweight replacement test run.

No repository-wide pytest.
No historical heavy audit suite.
No production code changes.
