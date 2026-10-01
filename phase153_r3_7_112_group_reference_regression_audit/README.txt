Phase153-R3-7
112-group Reference Regression Audit

目的
====
Phase153-R3-1〜R3-6 の結果を、n=2..15, k=0..7 の112群全体で再監査する。

production changes
==================
なし。

tests changes
=============
なし。

監査項目
========
1. Reference entries 数
2. representative statement が選択された entries 数
3. unresolved reference steps
4. public Narrative の Reference section に selected statement が実際に表示されているか
5. R3-5 後も selected statement の exact duplicate が本文に残っていないか
6. rule-name / type-name fallback が public Reference section に露出していないか
7. exceptions

重要
====
この監査は「監査スクリプトの完走」と「欠陥0件」を分ける。

欠陥が残っていても exit code 0 で完走し、
該当群・[Rn]・statement を CSV に出力する。
そのため、AUDIT COMPLETE WITH DEFECTS は実装失敗ではなく監査結果である。

出力
====
output/
- group_reference_regression.csv
- reference_entry_regression.csv
- selected_reference_statements.csv
- unresolved_reference_steps.csv
- public_reference_missing.csv
- body_exact_duplicates.csv
- public_reference_fallback_exposures.csv
- exception_inventory.csv
- reference_regression_summary.txt

完了条件
========
監査 package 自体:
- 112 groups を走査
- exceptions を記録
- 各欠陥を分類して出力
- production/test files を変更しない

R3 regression の理想状態:
- entries_without_selected_statement = 0
- unresolved_steps = 0
- public_reference_statement_missing = 0
- body_exact_duplicates = 0
- public_reference_fallback_exposures = 0
- exceptions = 0

次 Phase との境界
================
R3-7 は audit-only。
残存 defect があれば次 subphase でその分類だけを修正する。
すべて0なら Phase153 final regression / full pytest / documentation closure へ進む。
