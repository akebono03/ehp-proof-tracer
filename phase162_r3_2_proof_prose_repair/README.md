# Phase 162 R3-2 Proof Prose Repair

This patch repairs the lower, validated group-proof panel. The upper Group proof remains unchanged.

The previous R3 narrative collapsed the R7-validated EHP proof to a generic sentence and changed ASCII punctuation. The new R3 renderer reuses the existing detailed, independently validated EHP prose, removes only the subheadings, and adds the source group's existing proof as a separately labeled reference. The ultimate group equality comes from the R2 final proof step. No synthetic inference is created.

The source group reference is labeled as a previously proven result; no unverified literature attribution is made. Full literature attribution remains outside this repair.

## Installation

Extract this package into the repository root. In PowerShell execute `run_phase162_r3_2_proof_prose_repair.ps1` from within the extracted folder.

The script backs up the two replaced files and runs focused tests. The full suite is not run.

## Scope

- Modify `phase162_r3_narrative_connection.py`: `_element_latex`, add `_phase162_legacy_ehp_body` before `render_phase162_r3_narrative`, replace `render_phase162_r3_narrative`.
- Modify `tests/test_phase162_r3_narrative_connection.py` for the sole final QED marker.
- Add two focused regression test files inside this package.
- Leave all Web routing and the upper Group proof intact.
