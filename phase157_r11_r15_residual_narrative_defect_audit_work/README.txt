Phase157 R11-R15 — Residual Narrative Defect Audit

目的
====

R11-R14 focused pytest 62 passed 後の public Narrative を
112群で横断監査し、残存 defect candidate を分類する。

この audit は production/test code を変更しない。

対象
====

- n=2..15
- k=0..7
- 112 groups
- replay depth=2
- public Narrative renderer

監査 category
=============

1. visible_dependency_order
   ORDER / MAP_PROPERTY step について、premise と conclusion の両方が
   public body に一意に見える場合だけ、premise が後ろなら検出。

2. zero_map_used_without_visible_statement
   zero-map statement 自体が本文に出ていないのに、
   `Δ=0` の shorthand が本文で使われる場合を候補として検出。

3. possible_redundant_left_ehp_term
   E injective が既に見えている後で、
   Delta-E-H の4項 EHP sequence を再表示する場合を候補として検出。
   これは数学的誤りではなく presentation candidate。

4. standalone_connector
   `以上より,` / `したがって,` / `これより,`
   が単独 paragraph で残る場合。

5. repeated_numeric_equality
   `=4=4` のような同じ整数の重複 equality。

6. public_reference_without_body_marker
   Reference header はあるが本文に対応する [R#] marker が無い場合。

出力
====

- audit_output/summary.txt
- audit_output/findings.csv
- audit_output/exceptions.csv
- audit_output/narratives/<affected-group>.md

判定
====

これは closure gate ではない。
findings があっても audit 自体は成功扱い。
112群を走査できない、または render exception がある場合だけ exit 1。

pytest は実行しない。
全体 pytest は Phase157 closure まで実行しない。
