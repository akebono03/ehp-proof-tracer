Phase 155 Closure-R2C-R3-R1 — focused repair

Repairs exactly the three focused-verification failures from R2C-R3:

1. Add local `TodaGroupQuery` import to the two Phase96 lightweight tests.
2. Replace the stale Phase144-only audit-boundary assertion with a reviewed
   Phase144-or-Phase153 boundary assertion.

The audit-only manifest is already correct and remains unchanged:
- two Phase144 final completion audits;
- one Phase153 112-group duplicate audit.

No production changes.
No top-level import changes.
No 112-group audit execution.
No repository-wide pytest.
