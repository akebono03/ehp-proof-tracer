# GitHub baseline — Phase 155-R3-3C-r2

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before implementation:
- `tests/test_phase132_9_web_group_proof_modes.py`
- `tests/test_phase143_55b_conclusion_step_ordering.py`
- `toda_group_proof_narrative_transition_renderer.py`
- `web_group_proof.py`
- Phase 153 reference relevance / normalization tests
- Phase 154 reference-linkage tests

Current contract:
- pi16_9 source theorem metadata is `Toda Proposition 5.15`.
- root theorem provenance is distinct from supporting Reference selection.
- transition renderer returns `以上より, ` under the ASCII punctuation policy.

Therefore the three post-removal failures are stale historical expectations,
not duplicate-removal regressions.
