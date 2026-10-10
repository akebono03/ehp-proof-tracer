# Phase 163 R2 — 変更対象

- 新規 `unified_statement_registry.py`（リポジトリ直下）: `ReferenceKind`, `AssertionKind`, `AssertionOrigin`, `LiteratureEntry`, `AssertionEntry`, `AssertionInstantiation`, `ProofStepLink`, `UnifiedStatementRegistry`, `_nonempty`, `_positive_optional`。
- 新規 `tests/test_phase163_r2_unified_registry.py`: 軽量テスト6件。
- 既存のファイル・クラス・関数・テストの変更なし。

上記の新規 Python ファイルはいずれも全文であり、import を含めて省略はない。`run.ps1` はコピー後に対象テストのみ実行する。

## 境界

- `content` / `scope` は既存の Statement オブジェクトなどをそのまま格納できる不透明なフィールド。文字列から数学的命題を認識する機能ではない。
- 掲載位置 `publication_position`、同項目内 `component_position`、証明後利用可能位置 `available_after_position` は別情報。`None` は不明であり利用可能性を保証しない。
- 参照 ID / 主張 ID は数学的同一性の完全判定ではない。
- `ProofStepLink` は対応の記録のみで、ProofStep の改変や正当性判定をしない。
- R1 の全登録命題数は未確定のまま。R4 で既存 Registry の移行、Phase 164 で Backward Search 接続。循環依存グラフの完全検証、一般化された eligibility 判定は今回実装しない。

## 完了条件

新規データ型と軽量テストが通り、既存エンジンへの副作用がないこと。全体 pytest は Phase 終了時のみ実行する。
