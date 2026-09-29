Phase 144-6 Finalization R25-30 Boundary Gate

No production, existing test, or documentation files are changed.

The old R5-43-11D completion invariant hard-codes historical population counts.
The current pipeline reports three detached-but-insertable occurrences, so this
gate does not update those numbers blindly. Instead it runs the latest locally
retained R25-30 / argument-boundary-entry-classification pytest evidence and
three small production-route controls.

PASS means the old R5-43 snapshot is stale while the later R25-30 ownership
classification remains valid. FAIL means Phase 144-6 must not be closed yet.

This package does not run repository-wide pytest and does not implement Phase 145.
