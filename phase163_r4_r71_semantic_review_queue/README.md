# Phase 163 R4-R71: Context-cue Review Queue

This read-only package creates a reproducible review queue from the 237 pending R70 candidates. Textual signals and source overlaps are review hints, not mathematical classification or permission to register statements.

Run `run.ps1` from PowerShell after extracting into the project directory. Requires the existing `phase163_r4_r70_output/pending_batch_audit.json`, Python, and pytest. Only focused tests are run.

New files only: this Python audit, its 8 focused tests, `run.ps1`, and this README. No production registry changes and no IDs are allocated. Results are written into `phase163_r4_r71_output`.
