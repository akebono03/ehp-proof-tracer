# R10E4R1 変更一覧

## 変更対象

- `phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py` の `test_r10e2_guarded_patch_refuses_double_application()` のみ。
- 新規 `phase169_r10e4r1_historical_test_compatibility/patch_test.py`: 旧テスト 1 箇所のみを安全に更新する関数 `transform` と `main`、関数全文の抽出器 `_full_function`。
- 新規 `phase169_r10e4r1_historical_test_compatibility/tests/test_r10e4r1_historical_test_update.py`: 移行テスト。
- 新規 `run.ps1`: 履歴テストを更新し、元の R10E4 実行を呼び出す。

既存テストの import は変更しない。修正後のテスト関数全文は `test_r10e2_guarded_patch_refuses_double_application_FULL.py`、既存テストファイル全文は `test_r10e2_unpositioned_citation.FULL.py` を参照。実行時には現在の対象から生成した全文も `output` に保存する。

## 実行する pytest

1. R10E4R1 新規移行テスト2件。
2. R10E4 の既存 `run.ps1` が指定する限定テスト（前回 84 PASS / 1 FAIL だった範囲）。

## 完了条件

`R10E4R1_INTEGRITY_RESULT=PASS`、`R10E4_INTEGRITY_RESULT=PASS`、`R10E4_LIMITED_TESTS_AND_AUDIT=PASS` が揃うこと。

## 次の Phase との境界

R10E4R1 は互換性修復のみ。安定 stem の新しい文献命題、他の群の証明完成化、新しい一般的な推論規則は追加しない。
