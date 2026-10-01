Phase 153-R2 Follow-up
Reference / Semantic Fact All-Group Audit
=========================================

目的
----
current 112 groups に対して、literature reference を持つ leaf premise を
次の3分類へ分けて実測する。

1. reference_only
2. reference_plus_semantic_fact
3. unresolved_rendering

母集団
------
Phase 151 / Phase 152 と同じ。

- n = 2..15
- k = 0..7
- 112 groups
- proof depth = 2
- semantic closure 後の presentation

判定規則
--------
reference_only:
  provenance-only statement。

reference_plus_semantic_fact:
  provenance-only ではなく、generic renderer が rule-name / type-name /
  raw fallback を使わず意味表示できる。

unresolved_rendering:
  provenance-only ではないが、generic renderer が fallback に落ちる。
  public Narrative で rule-name を表示して埋め合わせる対象とはせず、
  semantic rendering defect として残す。

重要な境界
----------
- production code は変更しない。
- public route は変更しない。
- provenance-only catalog は変更しない。
- reference extraction / numbering は変更しない。
- statement renderer は追加しない。
- pytest 全体は実行しない。

出力
----
audit_output/reference_leaf_occurrences.csv
audit_output/reference_leaf_category_summary.csv
audit_output/reference_leaf_by_statement_type.csv
audit_output/exception_inventory.csv
audit_output/reference_leaf_summary.txt
audit_run_output.txt

この監査結果を見てから、reference marker と semantic fact の共存規則を
実装するかどうかを判断する。
