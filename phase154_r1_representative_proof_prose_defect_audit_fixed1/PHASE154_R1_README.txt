Phase 154-R1 — Representative proof prose defect audit

目的
----
現在の public Narrative route を変更せず、代表群の証明本文を同一条件で取得し、
不自然さを一般的な defect category（欠陥分類）に整理する。

production code の変更
----------------------
なし。

監査対象
--------
Primary:
- pi_6^3   : n=3, k=3
- pi_10^4  : n=4, k=6
- pi_11^4  : n=4, k=7

Secondary:
- pi_12^5  : n=5, k=7
- pi_16^9  : n=9, k=7

depth
-----
2

監査カテゴリ
------------
- transition_repetition
- semantic_duplication
- internal_rule_name_leakage
- english_statement_prose
- reference_body_linkage
- argument_contribution_ordering
- punctuation

注意
----
R1 は修正 Phase ではない。
機械検出結果だけで R2 を決めず、出力された Narrative と numbered proof body を目視確認する。
R2 では複数群に共通し、より上流の一般規則で説明できる defect category を1つだけ修正する。
pi_6^3 専用修正は行わない。
Test Suite Consolidation には触れない。

実行
----
リポジトリ直下にこのフォルダを展開し、PowerShell で次を実行する。

powershell -ExecutionPolicy Bypass `
  -File ".\phase154_r1_representative_proof_prose_defect_audit\run_phase154_r1_representative_proof_prose_defect_audit.ps1"

出力
----
phase154_r1_representative_proof_prose_defect_audit\phase154_r1_output\
  pi6_3_narrative.md
  pi10_4_narrative.md
  pi11_4_narrative.md
  pi12_5_narrative.md
  pi16_9_narrative.md
  phase154_r1_defect_report.md
  phase154_r1_defect_report.json
