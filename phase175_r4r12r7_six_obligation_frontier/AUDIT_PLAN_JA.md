# Phase 175 R4R12R7R1 — 監査済みコミット境界修正

- GitHub の `develop` は旧基準 `9203e1a8c077320a58214bda40d9bfeb17704f58` の直系1コミット先である `94c5d6839889bbfa03aad166ac9c6fd1558b8c5b` と確認。
- 変更対象: `phase175_r4r12r7_six_obligation_frontier/audit.py` の `verify_environment()` 全体、および `REVIEWED_HEAD` / `REVIEWED_COMMITTED_PATHS` 定数追加。
- テスト対象: 同パッケージ `tests/test_audit.py` の全体。追加テスト `test_reviewed_commit_pin_and_exact_diff()`。
- 許可されたコミット差分は GitHub の比較結果と完全一致が必要。これ以降のコミット、未承認の追跡コード変更は拒否する。
- 既存の `render` 検証、共有 Provider のコード検査、六つの ProofStep 前提は変更しない。
- 読み取り専用監査と限定 pytest のみ実行。全体 pytest は Phase 終了まで実施しない。
- 完了条件: `PASS_R4R12R7_SIX_OBLIGATION_FRONTIER_NOT_COMPLETE`。群の完成証明や新規 GIVEN は主張しない。
