# Phase 165 R48 — Structural exactness

Changes:
- `toda_group_proof_generic_narrative_renderer.py`: `_render_generic_narrative_proof_block`, adding reason output directly from a proof step's exactness premise.
- `toda_group_proof_narrative_renderer.py`: removes obsolete `_phase159_r1_6c_link_proof_reasons` and its call from `_phase159_r1_7c_preexisting_render_toda_group_proof_narrative_markdown`.
- `install.py`, `test_r48.py`, `run.ps1`: installation, 4 targeted tests, no full pytest.

The old linker combined exactness prose with an unrelated source citation specialization. This patch removes that legacy routine, rather than retaining a parallel path. Other possible string-matching routines have not been exhaustively removed; they require separate analysis. Reference general-form rendering remains incomplete.

Completion: four targeted tests pass and the public Narrative shows structural exactness reasons. The installer saves original source files before modification.
