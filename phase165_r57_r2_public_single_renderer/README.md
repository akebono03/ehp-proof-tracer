# Phase 165 R57-R2 — Single public Narrative entry

This package routes both completed and incomplete typed group searches to `render_toda_group_proof_narrative_markdown()`. Existing completed `TodaGroupProofPresentation` rendering remains unchanged. An incomplete search is not a completed presentation: its typed open goals remain explicitly unresolved and may never appear as proven statements.

The compatibility API `render_partial_proof_markdown()` now delegates to the public entry. The new `phase165_r57_r2_partial_narrative.py` holds a general, group-independent incomplete-state formatting helper, reusing the existing shared step prose renderer. There is no new group-specific text, inference rule, or proof source. This phase does **not** delete legacy helpers, which may still have direct external or test callers; removal requires separate dependency verification. It does not claim that the old partial layout and full presentation layout are internally identical, only that the production public entry is unified.

The installer backs up modified Python files, applies AST-anchored whole-function replacements, and refuses an inconsistent preexisting adapter. Run `run.ps1` from the extracted directory; it installs the patch and executes four focused test modules only. There is no full-suite pytest.
