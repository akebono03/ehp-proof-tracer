# Phase 166：追跡済み現行テストの終了監査

## 変更対象
新規 `close.py`: `candidate_classification()`、`tracked_inventory()`、`main()`。新規 `run.ps1`、`README.md`、`AUDIT.md`。既存コード・テストは変更しない。

## 調査結果
前回の入力 `test_inventory.json` には2,536採用、37除外、2構文エラー。エラーは歴史的バックアップにある。今回の監査は Git 管理下の `test_*.py` を採用し、アーカイブ・バックアップ・旧方式退避・監査結果を除外する。除外基準と全ファイル名を `manifest.json` に記録する。

## 判定
終了コード0でも `TESTS_PASS_PENDING_SCOPE_REVIEW` であり、無条件の正式完了ではない。`manifest.json` から収集漏れと必要な現行テストを確認する。終了コード非0なら `BLOCKED_TESTS`。

## Phase 167
証明探索・Narrative 修正にはまだ着手しない。
