# Phase 168 R3-7: Citation Cutover Gate

This incremental package adds a read-only validation boundary. It does not change the public rendering route. The gate compares citation identities and numbers already fixed in `ProofNarrativeModel` to the old long-form text, and rejects reuse when they differ. A passing gate verifies citation consistency, not mathematical prose equivalence.

Run `run.ps1` from the repository root on Windows PowerShell. The script installs one new module, runs four targeted tests, and reports findings for four proof goals. The full pytest suite is deliberately not run.
