Phase 151-3 — Cross-cutting Audit
====================================

目的
----
Phase 151-2 の112群baselineを再現した上で、
群ごとの修正候補ではなく、全群横断の共通パターンを抽出する。

production code変更なし。
existing tests変更なし。
Narrative文章・semantic role・fallbackは修正しない。

主な監査
--------
1. OTHER step と fallback step の重複
2. fallback が集中する statement type
3. rule-name fallback が集中する inference rule
4. fallback と block role の関係
5. stem k=0..7 ごとの集中
6. typed reason kind と conclusion type の関係
7. 群別の件数分布

Phase 151-2 baseline再現条件
----------------------------
groups = 112
presentation nodes = 713
blocks = 559
arguments = 129
OTHER blocks = 126
rule-name fallback = 115
type fallback = 51
raw fallback = 0
exceptions = 0

出力
----
audit_output/step_cross_cutting_inventory.csv
audit_output/statement_type_summary.csv
audit_output/rule_name_summary.csv
audit_output/block_role_fallback_summary.csv
audit_output/stem_summary.csv
audit_output/group_summary.csv
audit_output/reason_cross_cutting_summary.csv
audit_output/exception_inventory.csv
audit_output/cross_cutting_summary.txt

Phase境界
---------
Phase 151-3では「どの問題が何件あるか」「何と重なるか」まで。
原因分類は次のPhase 152で行う。

Phase 152では、151-3の結果を
selection / ownership / ordering / reason prose /
semantic naming / fallback / formatting / result reuse
などの defect category に整理する。

full historical regressionは実行しない。
