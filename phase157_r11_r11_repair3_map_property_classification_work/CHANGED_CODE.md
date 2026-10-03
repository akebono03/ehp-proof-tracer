# Phase157 R11-R11 repair3

変更対象:

1. `toda_proof_dependency.py`
   - import に `TodaHopfInvariantSurjectiveStatement` を追加。
   - `classify_toda_proof_step_role()` の MAP_PROPERTY 判定対象へ追加。

2. `toda_group_proof_narrative_contribution_renderer.py`
   - `suppress_toda_group_proof_narrative_reference_body_duplicates()`
   - standalone statement の末尾 `,` / `.` を無視して同一視。
   - `[R#]より, ... .` と表示。

3. `tests/test_phase157_r11_reference_reason_punctuation.py`
   - H-surjectivity dependency-role regression test を追加。

Focused pytest:
- Phase157 R11
- Phase157 R5/R9/R10
- Phase148 semantic closure
- Phase93 dependency role classification

全体 pytest はまだ実行しない。
