# Phase 168 R3-39D — Existing-rule repair

This local PowerShell package reuses the already registered generic scalar specialization rule. It fixes the typed iota-family matching, registers the missing symbolic circle clause in the existing (5.1) registration, and prevents four legacy direct leaves from bypassing universal sources in the default shared context. Existing assertions remain in the registry for compatibility.

It does not add a renderer, goal-specific proof, or independent expansion rule. The installer refuses unknown code anchors and saves complete replacement files in `full_files/` and originals in `backup/`. It runs only focused pytest, including three-group search integration. The full suite is reserved for Phase 168 closure.

**Status:** Prepared but not executed against the complete Windows repository. The integration test must pass before treating this change as accepted.
