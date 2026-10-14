# Phase 165 R57-R2 実装・監査

## 変更対象

1. `toda_group_proof_narrative_renderer.py`：末尾の `render_toda_group_proof_narrative_markdown()` を関数全文置換。既存 import 不変更。
2. `phase165_r52_partial_proof.py`：`render_partial_proof_markdown()` を関数全文置換。既存 import 不変更。
3. 新規 `phase165_r57_r2_partial_narrative.py`：ファイル先頭に共通の未完成証明表示関数 `_partial_statement_math()`、`render_incomplete_public_narrative()` を追加。
4. 新規 `test_phase165_r57_r2_public_single_renderer.py`：4件の対象テスト。
5. `install.py` と `run.ps1`：バックアップ、適用、対象テスト。

## 設計上の境界

完成証明は以前の Presentation と公開 Renderer の処理を維持。未完成証明は完成済み根を作り出さず、証明済み ProofStep と未解決 Goal を明示的に分離する。外部から呼び出す公開 Renderer を統一するが、旧未完成表示関数の本体は互換性のため残す。これは**旧方式の物理削除完了ではない**。

## 実行 pytest

`python -m pytest -q phase165_r57_r2_public_single_renderer/test_phase165_r57_r2_public_single_renderer.py phase165_r56_r2_public_renderer/test_phase165_r56_r2_public_renderer.py phase165_r57_r1_single_entry/test_phase165_r57_r1_single_entry.py phase165_r55_nk_only_web/test_phase165_r55_nk_only_goal.py`

## 完了条件

上記対象テストが成功し、完成証明は元の公開 Narrative と一致、未完成証明は公開入口から表示され、未解決 Goal に結論記号 `□` が付かないこと。全体 pytest は Phase 165 完了時だけ実行する。

## 次段階

旧 `render_toda_partial_proof_narrative_markdown()`、群別専用 Web 関数、旧 CLI/群構造探索入口の直接利用とテスト・外部依存を監査して削除。必要な数式生成の共通部品は残す。
