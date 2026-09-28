Phase 144-6-R5-43-10-R3 direct-connector regression update

Production code changes: none.

Reason:
R5-43-4 originally asserted that the entire connector map had exactly one
entry. R5-43-10 intentionally adds one transport-compression connector, so the
map now correctly has two entries for pi_6^3:
- one transport-compression connector;
- one direct dependency connector, "これより、".

The R5-43-4 regression is updated to assert its actual invariant:
only the direct dependency C4 -> C5 receives the direct connector "これより、".

All other R5-43-4 tests are unchanged.
No public route change.
No full test suite.
