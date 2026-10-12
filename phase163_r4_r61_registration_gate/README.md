# Phase 163 R4-R61: Pre-registration gate

This read-only audit cross-checks the R4-R58 archival readiness assessment, R4-R59 synthetic insertion and ID invariance experiment, and R4-R60 live registry collision audit.

Run `run.ps1` from the extracted `phase163_r4_r61_registration_gate` folder beneath the project root. It requires the previous phase outputs in their standard project subdirectories. Python and pytest must be installed. The script runs only nine focused tests and generates `phase163_r4_r61_output/registration_gate.json`, `registration_gate.csv`, and `report.md`.

This does not allocate production IDs, modify a registry, verify mathematical equivalence, or authorize proof-search use. Synthetic insertion positions from R4-R59 do not represent actual literature positions. Full pytest is deliberately not run.
