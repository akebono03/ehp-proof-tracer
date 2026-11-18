# Phase 175 R4R12R6 — Read-only Candidate Dispatch Trace

This audit checks whether the existing, repaired R4R3 quotient rule produces two
conditional EHP proposals and whether R4R12's public provider is called from
shared search and returns them. It changes no production code or proof records.

Extract into the repository root on branch `develop`, with the reviewed
`9203e1a8c077320a58214bda40d9bfeb17704f58` HEAD. Run
`powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r6_public_candidate_trace\run.ps1 -DryRun`
then run without `-DryRun`.

This is a diagnostic gate only. It neither proves the root group nor runs the
project-wide test suite. No new GIVEN statement or mathematical rule is added.
