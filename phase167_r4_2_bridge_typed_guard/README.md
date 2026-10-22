# Phase 167 R4-2: typed suspension bridge deduplication

Only one existing function is changed: `insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges` in `toda_group_proof_narrative_contribution_renderer.py`. A local typed guard skips inserting a redundant auxiliary bridge when the consuming ProofStep already concludes the same generator suspension. No generator names, group indices, output strings, proof steps or registries are modified. The guard compares generator symbols, dimensions, source/target, and the suspension map type; unrelated bridges remain unchanged.

Run `run.ps1` from the repository root. The script captures five 1-stem narratives, makes the patch, verifies that exactly one equation disappears in pi4^3 and the others remain identical, runs targeted pytest and restores the original on failure. Full pytest is intentionally not run. The full modified function is emitted to `modified_function_full.py.txt`.
