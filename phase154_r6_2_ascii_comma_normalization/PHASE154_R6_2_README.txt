Phase 154-R6-2 — ASCII comma normalization

正しい punctuation policy
-------------------------
- 読点: `, `
- 句点: `.`
- TeX / 数式内部の punctuation は変更しない
- Reference title の `Proposition 5.8.` 等は変更しない

変更対象 production
-------------------
1. toda_group_proof_generic_narrative_renderer.py
   - `_generic_short_exact_sequence_reason_prose`

2. toda_group_proof_narrative_reason_renderer.py
   - `render_toda_group_proof_narrative_reason_sentence`

3. toda_group_proof_narrative_argument_discourse.py
   - `render_toda_group_proof_narrative_argument_discourse_marker`

4. toda_group_proof_narrative_argument_renderer.py
   - `render_toda_group_proof_narrative_argument_header_method_section`

5. toda_group_proof_narrative_contribution_renderer.py
   - contribution connector prose
   - `suppress_toda_group_proof_narrative_reference_body_duplicates`
   - `link_toda_group_proof_narrative_reference_body_consumers`

6. toda_group_proof_narrative_renderer.py
   - `_append_narrative_for_step`
   - `render_toda_group_proof_narrative_markdown`
   - legacy Narrative connectors

import 変更
-----------
なし。

実装方針
--------
上記 Narrative renderer source 内の Japanese comma `、` を
ASCII comma + space `, ` に変更する。

final-render の一括置換は行わない。
TeX renderer や数式 source は変更しない。

テスト
------
新規:
- tests/test_phase154_r6_2_ascii_comma_normalization.py

current punctuation contract を直接確認する既存テストだけ
`、` -> `, ` に更新する。

完了条件
--------
- focused tests PASS
- 5代表群で
  `TOTAL japanese_period_sentence_endings: 0`
- 5代表群で
  `TOTAL japanese_comma_prose_lines: 0`
- ASCII period が存在する
- ASCII comma prose が存在する
- R5 Reference linkage を維持
- Reference title punctuation を維持

全体テスト
----------
実行しない。Phase 154 の最後にのみ実行する。

次
----
R6-2 完了後は Phase 154 punctuation closure audit を行い、
その後 Phase 154 全体の closure / full regression に進む。
