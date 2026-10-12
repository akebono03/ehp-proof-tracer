Phase 164 R9 — shared public Narrative normalization, targeted only.

Extract ZIP at project root, then run:
  powershell -ExecutionPolicy Bypass -File ".\phase164_r9_web_narrative\run.ps1"

Changes:
 - phase164_r9_narrative_contract.py: newly added shared formatter
 - toda_group_proof_narrative_renderer.py: final public function only
 - no changes to proof tree, registries, or other Phase code

Normalization scope:
 - Remove an EXACT EHP display math subwindow if already visible within an earlier complete sequence
 - Remove duplicate adjacent standalone exactness connectors
 - Normalize redundant '完全性より, これより,'
 - Preserve all conclusions, references, numbered statements, and mathematical reasoning

After execution, manually inspect n=3, k=2, depth=2 in Web view. The initial displayed output may use math delimiters or multi-line formatting not handled by this conservative pass; audit.json does not claim visual closure.

Only focused pytest runs; no full pytest until Phase 164 closes.
