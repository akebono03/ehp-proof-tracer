# Phase 176 R3R41 — Public Toda (5.5) connection

This package connects the R3R40R1 audited backward plan to the default shared expansion provider. It derives the candidate from the requested typed Hopf equality and screened source conclusions. It does not supply proof steps, new GIVEN statements, or new inference rules. Independent R3R39 and Toda (5.5) obligations are reconstructed by the normal DFS.

Run `run.ps1 -DryRun`, then `run.ps1` from the repository root. The patch adds eight LF lines to `shared_expansion_provider`; no global imports are modified. The full updated function is exported to `SHARED_FUNCTION_FULL_JA.md` on execution. The audit requires the existing R3R40 and R3R40R1 packages. It verifies every expected step of the resulting default shared DFS proof and its screened source ancestors. The focused test set includes the previous 33 tests, five public connection tests, and five scoped installer regression tests. No full pytest is run.

The DB generator's nu-prime representation remains an open boundary. This phase does not claim a registered-generator Hopf image or a completed group proof. If an audit fails, do not commit the patch until the failure is resolved. The installer is idempotent and rejects mixed/CRLF source or a partial patch.

## R3R41R1 — Installer scope repair

The original DryRun incorrectly required a module import to appear only once in the entire shared file. The reviewed develop file legitimately imports two different symbols from the same module. The installer now locates the unique top-level `shared_expansion_provider` and its immediate nested `expand` using AST, and checks the complete multi-line dispatch anchor inside that scope. It rejects incomplete or moved patches and preserves LF bytes. The mathematical provider and audit are unchanged. Re-extract this package over the existing R3R41 directory and run the same script. The focused suite is expected to contain 43 cases.
