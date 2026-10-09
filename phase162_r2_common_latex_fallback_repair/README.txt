Phase 162 R2 repair — existing mathematical LaTeX fallback

Cause: generic _render_generic_narrative_step returns the inference rule name for TodaPi32WhiteheadSquareUpToSignStatement.
Fix: when generic prose is missing, reuse _render_group_proof_narrative_latex from the existing common group narrative renderer.
No statement-specific text, rule changes, Phase 161 changes, Reference changes, or Web changes.
The two modified files are complete replacements in files/.
Run run_phase162_r2_repair.ps1 from repository root after extracting the zip.
Focused pytest only. Whole suite remains deferred to Phase 162 closure.
