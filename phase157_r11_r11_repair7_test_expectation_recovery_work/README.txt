Phase157 R11-R11 repair7 — test expectation recovery

repair6 は production ordering function の置換まで成功したが、
historical test の文字列検索で patch script が停止した。

したがって local repository では:
- production code: repair6 ordering change 適用済み
- historical test expectation: 未更新
- focused pytest: 未実行

repair7 は production code を変更しない。

変更:
- tests/test_phase157_r5_r9_fixed_definition_body_suppression.py
- test_phase157_r5_r9_fixed_definition_remains_in_reference() 全体を置換
- membership Reference line の期待を `,` から `.` に更新

その後:
- syntax check
- R11/R5/R9/R10/Phase148/Phase93 focused pytest
- pi_6^3 narrative を表示

full repository pytest は Phase157 closure まで実行しない。
