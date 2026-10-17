# Phase 165: Group-specific adapter removal audit R2

This package **does not modify production code**. It independently checks that the retired `phase165_r52_r23_existing_rule_adapter.py` file does not exist, that no top-level importable Python module refers to its import or `expand_existing_pi43_rules`, and that the shared provider retains generic, witness-backed, and seeded candidate-generation connections.

Run `run.ps1` after extracting the archive into the repository root. The read-only results are written to `audit_result.json`. Only four focused pytest tests are run. An audit pass is **not** proof that a generic EHP proof of pi_4^3 completes. Inactive archived sources and subdirectories are not claimed to be deleted.
