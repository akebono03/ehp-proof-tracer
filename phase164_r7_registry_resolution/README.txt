Phase 164 R7: Registry-backed statement resolution (targeted migration)

Changes:
* new phase164_r7_statement_resolution.py - centralized, read-only resolution and citation checks
* phase164_r3_registry_search_connection.py - route registered literature premise lookup through resolver
* new tests/test_phase164_r7_statement_resolution.py - focused identity, provenance and fail-closed cases

The proof repository continues to hold ProofSteps; registry holds statement identities.
This does NOT migrate every existing repository lookup. It is a tested first connection,
not completion of system-wide R7. No proof derivation or rendering changes.

Run run.ps1 after extracting this directory in repository root.
Installer verifies the exact original R3 Git blob SHA. If it differs, nothing
is changed and local source must be inspected first.
Full pytest suite is intentionally NOT run.
