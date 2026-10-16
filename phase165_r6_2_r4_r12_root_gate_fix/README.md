# Phase 165 R6-2 R4-R12

This patch adjusts the common root proof-order gate to admit structurally verified scalar instances of two registered specialization rules. It does not add citations, treat a goal as proof, or bypass the downstream requirement for fixed typed GIVEN evidence. All other root cycles remain rejected.

Run `run.ps1` from the extracted package on Windows PowerShell. The installer preserves a backup and edits only `is_unordered_root_structure_specialization` and the new helper preceding it in `phase165_r57_r11_proof_order_gate.py`.

The full suite is reserved for the end of Phase 165.
