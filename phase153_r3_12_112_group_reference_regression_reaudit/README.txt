Phase153-R3-12
112-group Reference Regression Re-Audit

目的
====
Phase153-R3-9〜R3-11 後の Reference pipeline を
112 groups 全体で再監査し、R3 closure 条件を確認する。

対象
====
n=2..15
k=0..7
合計112 groups
depth=2
semantic closure

production changes
==================
なし。

tests changes
=============
なし。

route-neutral boundary
======================
R3-10 で判明した
"## 証明対象" と "## 証明" の substring 混同を避ける。

1. splitlines() 上で "## 証明" が完全一致する route
   -> その前を Reference section、その後を body とする。

2. "## 証明" がない route
   -> canonical structured Reference section が public output の先頭なら、
      その canonical section を Reference section とする。

closure metrics
===============
以下がすべて 0 なら R3 CLOSURE: PASS。

- exceptions
- entries without selected statement
- unresolved reference steps
- public selected statement missing
- public Reference marker missing
- exact selected statement duplicated in proof body
- rule-name/type-name fallback exposure in Reference

出力
====
output/
- reference_regression_summary.txt
- route_inventory.csv
- entries_without_selected_statement.csv
- unresolved_reference_steps.csv
- public_selected_statement_missing.csv
- public_reference_marker_missing.csv
- exact_body_duplicates.csv
- reference_fallback_exposures.csv
- exception_inventory.csv

次 Phase との境界
================
R3-12 は再監査のみ。
closure PASS の場合、R3 を完了候補とする。
Phase153 全体の最終テスト・documentation closure は別途行う。
