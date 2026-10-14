# Phase 165 R27-R22

Replace the standard Web Group Query's legacy calculation dependency with the common typed Backward Search.

Run `run.ps1` from the repository root after extracting the archive. The installer checks the old source structure, writes a backup and runs only three targeted tests. It does not run the full suite.

This change intentionally maps unproved and partial group structures to the existing `NOT_FOUND` query status; details remain available through the group-proof progress view. No legacy proof result is promoted to `FOUND`.
