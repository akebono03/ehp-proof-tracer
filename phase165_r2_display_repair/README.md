# Phase 165 R2 — Existing Narrative Renderer Repair

Run `run.ps1` from the project root in PowerShell. This patch modifies only `toda_group_proof_narrative_renderer.py`, specifically its existing `render_toda_group_proof_narrative_markdown` function. The script saves the complete original file, captures the pre-change pi3_2 public Narrative, applies the patch, and validates pi3_2 equality and pi4_3 essential facts. On verification failure it restores the original renderer. It does not run the full test suite and does not verify physical browser rendering.

The patch reuses the existing typed kernel/quotient statement classes and formatting helpers. It does not change proof search or add a renderer module. The complete replacement function is constructed in `patch.py` from the current original function. No GitHub writes are made.

R3 architectural guarantees and full end-to-end browser verification remain out of scope. Review the output files and run browser checks before declaring R2 completed.
