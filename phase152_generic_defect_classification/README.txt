Phase 152 — Generic Defect Classification
==========================================

目的
----
Phase 151-3 の全群横断結果を、修正単位となる defect category に分類する。
このPhaseでは production code を変更しない。

確認済みカテゴリの定義
----------------------
1. semantic_classification_and_statement_rendering
   OTHER かつ fallback。
   semantic role と statement rendering の双方に未解決部分がある。

2. semantic_classification
   OTHER だが fallback ではない。
   rendererは表示できるが、数学的role分類が未解決。

3. statement_rendering
   fallback だが OTHER ではない。
   semantic role は既に分類されているが、generic statement rendering が不足。

4. reason_coverage
   typed reason が final_result_derivation に集中しているという横断的coverage gap。
   step-level fallback分類とは別軸。

Phase 152で断定しないカテゴリ
-----------------------------
selection
ownership
ordering
formatting
result_reuse

これらはPhase 151の件数baselineだけでは原因を証明できない。
必要なら後続Phaseで専用 invariant audit を行う。

Phase 151-3 baseline
--------------------
groups = 112
exceptions = 0
presentation nodes = 713
blocks = 559
arguments = 129
OTHER blocks = 126
OTHER steps = 144
fallback steps = 166
rule-name = 115
type-name = 51
raw = 0
OTHER ∩ fallback = 125
typed reasons = 146

期待されるstep-level partition
------------------------------
semantic_classification_and_statement_rendering = 125
semantic_classification = 19
statement_rendering = 41

出力
----
audit_output/confirmed_step_defect_categories.csv
audit_output/defect_by_statement_type.csv
audit_output/step_classification_inventory.csv
audit_output/reason_coverage_classification.csv
audit_output/unresolved_candidate_categories.csv
audit_output/exception_inventory.csv
audit_output/defect_classification_summary.txt

Phase境界
---------
Phase 152では分類だけを行う。
semantic role、renderer、reason kind、public routeは変更しない。

Phase 153では確認済み defect category を1つだけ選び、
minimum general rule -> focused tests -> 112群再生成
の順で修正する。
