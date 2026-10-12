# Phase 163 R4-R60 — ID Collision Audit

This package checks three R4-R59 trial definitions against IDs actually present in the runtime registry bridge. It never registers statements or allocates IDs.

From the project root, extract the ZIP and run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r60_collision_audit\run.ps1`.

Requires `phase163_r4_r59_output\id_order_trial.json` and the existing project modules. Writes `phase163_r4_r60_output\collision_audit.json`, `collision_audit.csv`, and `report.md`.

An equal locator with a different ID is flagged for review, not declared a mathematical duplicate. No formal mathematical equivalence is established. Only focused tests run.
