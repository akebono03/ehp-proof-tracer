# 変更一覧

- 新規 `phase165_r52_r18_proof_order.py`：`ProofUseOrder` クラス、`restrict_by_proof_use_order()` 関数（全文は同梱ファイル）。
- 変更 `phase165_r52_r9_shared_math.py`：`search_shared_group_goal()` に `proof_use_order=None` を追加し、R16 スクリーニング後・推論候補生成前に制限を適用。
- 新規 `test_phase165_r52_r18_proof_order.py`：全7テストと import を同梱。
- `run.ps1`：対象 pytest のみ実行。

## 境界

この R18 は明示した `ProofUseOrder` に対する汎用の判定と検索接続だけを実装する。Proposition 5.1 の4成分への自動同定・本番での順序自動設定は含めない。文献順と証明順を混同しない。
