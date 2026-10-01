Phase153-R3-8
Remaining Reference Defect Classification

目的
====
Phase153-R3-7 で残った欠陥を原因別に分類する。

対象
====
- unresolved steps: 31
- entries without selected statement: 14
- public Reference statement missing: 17
- exact body duplicates: 149

production changes
==================
なし。

tests changes
=============
なし。

分類軸
======
A. unresolved
- statement type
- fallback kind
- Reference
- affected groups

B. selected statement なし
- unresolved_only_or_unrenderable
- no_renderable_candidate
- selection_returned_empty

C. public missing
- public renderer route shape
- ## 証明 の有無
- [Rn] marker の有無

D. body duplicate
- standalone_line
- reference_marker_sentence
- embedded_without_reference_marker
- route shape
- affected groups

解釈
====
- unresolved_only_or_unrenderable が中心
  -> renderer coverage の修正候補
- selection_returned_empty
  -> representative selection rule の修正候補
- custom/no-proof route に public missing が集中
  -> public route connection の修正候補
- standard route で exact duplicate が集中
  -> suppression timing/coverage の修正候補
- embedded_without_reference_marker が多い
  -> body ownership / generation の修正候補

出力
====
output/
- unresolved_by_occurrence.csv
- entries_without_selected_statement.csv
- public_missing_classification.csv
- body_duplicate_classification.csv
- route_inventory.csv
- exception_inventory.csv
- remaining_reference_defect_summary.txt

次 Phase との境界
================
R3-8 は classification audit のみ。
修正は監査結果を見て次 subphase に分割する。
