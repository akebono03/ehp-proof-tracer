Phase 155 Closure-R2C-R3 — remaining six lightweight replacements + one audit-only test

Boundary
--------
R2C-R1 classified 9 LIGHTWEIGHT_REPLACE tests.
R2C-R2 replaced the 3 extreme tests.
R2C-R3 validates that the exact remaining set is 6 before editing.

Lightweight replacements
------------------------
- Phase95 actual representative provenance: 2
- Phase96 source presentation provenance: 3
- Phase98 facade delegation: 1

The actual pi_9^5 EHP mathematical extraction remains covered by the dedicated
Phase92/93 tests. R2C-R3 removes duplicate reconstruction of that heavy proof
fixture from the Phase95 metadata contract.

Audit-only
----------
The 112-group exact selected-statement duplicate scan remains in the repository
but is added to `tests/phase155_audit_only_nodeids.txt`. It is not run in
routine pytest.

No production code changes.
No repository-wide pytest.
