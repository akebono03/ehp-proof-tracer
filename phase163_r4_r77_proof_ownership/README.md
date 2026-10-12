# Phase 163 R4-R77 — Explicit Proof Attachment

This read-only check traces the 11 R76 entries to explicit Proof and QED markers in the frozen Toda TeX extracts. It does not judge mathematical correctness, assign Statement IDs, or alter the production registry.

From the project root, extract this bundle and run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r77_proof_ownership\run.ps1`. Requires the previous R76 output and the R42 TeX extracts.

The script writes `phase163_r4_r77_output/proof_ownership.json`, CSV, and `report.md`. Only nine focused tests are run. The full pytest suite remains deferred until Phase 163 ends.
