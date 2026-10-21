# Phase 166 R3-AF テストデータ修正

## 変更対象

- `phase166_r3af_goal_source/tests/test_r3af.py`
  - `test_unsupported_generator_fails_closed()`（関数全体を同梱ファイルに収録）

既存テストの import 部分も含めたファイル全文を `test_r3af.py` に収録。`SphereRepository.get_group()` が必須とする `Element`、`gen_coe` の列をテスト CSV に追加する。未対応の `unknown` 生成元が空候補 `()` になるという検査は維持する。

本体コード・命題台帳・証明探索規則は変更しない。限定 pytest のみ実施し、Phase 166 終了前には全体 pytest を行わない。
