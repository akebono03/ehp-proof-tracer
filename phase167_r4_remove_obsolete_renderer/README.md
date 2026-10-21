# Phase 167 R4 — Remove obsolete alternative Narrative renderer

This patch removes the unused `render_completed_from_proofsteps` function and its private helpers without removing the shared ancestry utilities. It also removes the adapter's conditional routing to that renderer. The sole destination for completed adapter output becomes the existing `render_toda_group_proof_narrative_markdown`.

Changed production files:

- `phase165_r56_presentation_adapter.py`: replace the entire `render_completed_shared_narrative` function. No top-level imports changed.
- `phase165_r57_r10_step_narrative.py`: delete `render_completed_from_proofsteps`, `_math_statement`, `_reference_label`, and their unused imports. Preserve `ordered_proof_ancestry` and `has_transport_proof_ancestry`.

No 2-stem validation is included. Targets: pi3^2, pi4^3, pi5^4, pi6^5, pi7^6 only (1-stem). Before/after comparison includes search status, proof records, markdown and web lines. A changed result fails the run and restores both production files. Targeted pytest only; no complete suite.

Run the PowerShell script from the repository root. The installation script checks for the expected old functions before edits; take a commit/snapshot first if you have unrelated local changes.
