# Phase 163 R4-R88 JSON integrity fix

This package replaces the distribution-only R88 runner. No production source code is modified.

The old runner compared SHA-256 of entire JSON files and rejected equivalent data with different whitespace or formatting. The new runner compares the complete parsed JSON values against the reviewed R86 and R87 snapshots. Any changed field, missing record, or altered approval flag is rejected.

The source-grounded R88 claim checks remain unchanged. This package never promotes source archives to mathematically verified statements, allocates permanent IDs, or enables proof search.

Run from the project root using `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r88_json_integrity_fix\run.ps1` after extracting the ZIP there. Outputs go to `phase163_r4_r88_output` and only focused tests run.
