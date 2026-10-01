Phase 154 punctuation closure audit

目的
----
R6-1 / R6-2 で確定した punctuation policy:

- 読点: `, `
- 句点: `.`

が、5代表群だけでなく public Narrative renderer の
全112群に適用されているかを監査する。

監査範囲
--------
- n = 2..15
- k = 0..7
- 14 × 8 = 112 groups
- replay depth = 2
- public Narrative renderer

Phase 151 all-group audit と同じ母集団を使う。

監査対象
--------
Narrative prose の:
- Japanese comma `、`
- Japanese period `。`

監査対象外
----------
- inline TeX / math
- display TeX / math

Reference title の `Proposition 5.8.` など ASCII period は
正しいものとして保持する。

production 変更
---------------
なし。

既存 test 変更
--------------
なし。

audit output
------------
- audit_output/summary.txt
- audit_output/violations.csv
- audit_output/exceptions.csv

focused tests
-------------
- tests/test_phase154_r6_2_ascii_comma_normalization.py
- tests/test_phase154_r6_2_repair1_missing_shared_sources.py
- tests/test_phase154_r6_2_repair2_equation_numbering.py
- tests/test_phase154_r6_1_repair3_ascii_period_policy.py

全体 test
---------
実行しない。
Phase 154 の最後にのみ実行する。

完了条件
--------
- scanned groups = 112
- rendered groups = 112
- exceptions = 0
- japanese comma violations = 0
- japanese period violations = 0
- ASCII comma prose が存在
- ASCII period prose が存在

FAIL の場合
-----------
この audit では production を変更しない。

`violations.csv` の group / section / line を使って
残存 source を分類し、Phase 154 punctuation closure repair
として最小修正する。

PASS の場合
-----------
Phase 154 punctuation は closure 完了。

次:
- Phase 154 closure audit
- documentation closure
- phase-end full regression
