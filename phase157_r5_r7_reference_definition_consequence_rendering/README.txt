Phase157-R5-R7 — Reference definition/consequence rendering

目的:
同一 Reference 内で fixed definition と fixed consequences が
一緒に選択された場合、definition -> consequences の関係を表示する。

今回の期待表示:
ν' ∈ {η_3, 2ι_4, η_4}_1 とすると,
ν' ∈ π_6^3,
2ν' = η_3η_4η_5.

変更対象:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r5_r7_reference_definition_consequence_rendering.py

production import:
- TodaLiteratureStatementClassification
- classify_toda_literature_statement_step

新規 helper:
- _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines

変更 function:
- _toda_group_proof_narrative_reference_statement_lines_by_number

一般規則:
- FIXED_STATEMENT の component_key が *_definition のものが
  ちょうど1件あり、選択 statement が2件以上の場合のみ適用。
- definition を先頭にする。
- definition に「とすると,」を付ける。
- 中間 consequence に「,」。
- 最後の consequence に「.」。

Proof body、fixed catalog、eligibility、argument ordering は変更しない。
