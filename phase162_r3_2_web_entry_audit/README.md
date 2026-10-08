# Phase 162 R3-2 Web entrypoint audit

This package is read-only. It does not change existing implementation or tests.

It locates the locally installed Phase 162 verified proof panel and records nearby source lines and relevant function names in `phase162_r3_2_web_entry_audit.json`.

The GitHub default branch does not currently expose `phase162_web_narrative_integration.py`, so blindly replacing the lower panel could damage the upper Group proof. Actual R3-2 route modification remains pending until the local panel entrypoint is examined.

Run `run_phase162_r3_2_web_entry_audit.ps1` from the extracted folder in the repository root.
