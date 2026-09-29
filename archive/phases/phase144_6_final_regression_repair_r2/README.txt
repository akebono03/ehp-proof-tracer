Phase 144-6 Final Regression Repair R2
======================================

目的
----
Final Regression Repair の focused test runner に、
Phase 144-6 Final Full Suite R4 で確立した dual-import 環境を適用する。

直前の失敗
----------
test_phase144_6_public_route_cutover.py の collection 中に、

  from tests.test_phase143_19_method_evidence import ...

が解決できず停止した。

これは Final Regression Repair で置換した9テストの内容による失敗ではなく、
focused runner が tests package style を成立させていなかったことが原因。

R2の変更
--------
Production code: 変更なし
Test code: 変更なし
Documentation: 変更なし
Runner: run_phase144_6_final_regression_repair_r2.ps1 のみ

実行環境
--------
一時 tests/__init__.py を作成し、
PYTHONPATH に次の両方を設定する。

- repository root
- repository root/tests

これにより、

  from tests.test_phase... import ...
  from test_phase... import ...

の両形式を同時に解決する。

runner が作成した tests/__init__.py は終了時に削除し、
元の PYTHONPATH も復元する。

完了条件
--------
1. Focused dual import preflight: PASS
2. Final Regression Repair 対象テスト: 全件 PASS

PASS後はテストを追加変更せず、
Phase末の canonical full suite R4 を再実行する。
