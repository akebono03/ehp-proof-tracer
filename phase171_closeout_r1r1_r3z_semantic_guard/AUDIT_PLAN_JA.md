# Phase 171 Closeout R1R1 — 旧ステップ数固定テストの最小修正

## 監査の根拠

- 対象 GitHub：`akebono03/ehp-proof-tracer` の `develop`。
- 監査済み HEAD：`e814ec939652807d464fd76051d34a9da40328f8`。
- R1 の限定 pytest：17ファイル収集、`87 passed, 1 failed`。
- 失敗：Phase 169 R3Z の `assert len(model.steps) == 28`、現在は 27。
- `phase168_r3_4_link_bridge.py` は既存の検索結果を `build_proof_narrative_model()` に渡す。
- `phase168_r3_3_proof_narrative_model.py` は `steps = result.proven_steps` とし、表示時に証明ステップを削除しない。

## 変更対象（必要最小限）

| 種別 | ファイル／要素 | 変更 |
|---|---|---|
| 既存テスト | `phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py` の `test_r3z_general_higher_eta_is_reference_only` | 28件固定を証明モデル同一性・推論根・未解決目標なしの意味検査へ変更 |
| 追加監査パッケージ | `phase171_closeout_r1r1_r3z_semantic_guard/install.py` | レビュー済み Git blob・編集範囲ガード、限定 pytest、失敗時ロールバック |
| 追加監査テスト | 同パッケージの `tests/test_install.py` | 5件：元ファイル照合、単一置換、未知内容拒否、CRLF・BOM保持、Git status の先頭空白保持 |

**変更しないもの**：既存テストの import、他の二つの既存テスト関数、本番の探索・Proof Tree・Renderer・Reference、`README.md` と `docs/` 内の正式文書。

## 合否判定

1. `-DryRun` が `PASS_DRY_RUN`。
2. 5件の監査パッケージテストが PASS。
3. R1 と同一17ファイルの限定 pytest が全件 PASS。
4. `git diff --stat` は上記の既存テストファイル1件のみで、未追跡の監査パッケージは別扱い。
5. `FULL_PYTEST_EXECUTED=False`。全体テストは文書更新を含めた Phase 171 終了時まで行わない。

実際のテスト結果は、ローカル PowerShell 実行の監査ログで確定する。公開証明や Reference に問題が出た場合、27件を無条件に正解と認定しない。

## Phase 境界

本修正は Phase 171 Closeout の R1 回帰テスト故障への対応のみ。文書更新・全体 pytest・最終完了宣言は別工程。Phase 172 の文章冗長性改善を先取りしない。
