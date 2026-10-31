# Phase 171 Closeout R2R1 — HEAD・コミット済み R1R1 の監査修正

## 根本原因

R2 の `current_files()` は `HEAD == e814ec939652807d464fd76051d34a9da40328f8` を要求し、さらに R1R1 のテスト変更が未コミットのままであることを要求していた。2026-10-31 に GitHub `develop` が `3e74849bf90bc115c16503ddd46d49996baa0856` へ進み、R1/R1R1 の成果と R1R1 テスト変更がコミットされたため、正しい作業環境が拒否された。

## 変更対象

- `phase171_closeout_r2_documentation_full_output/update_docs.py`：定数 `R1R1_COMMITTED_BLOB` を追加、`current_files()` と `main()` を全文置換。
- `phase171_closeout_r2_documentation_full_output/tests/test_document_writer.py`：後続コミット受理と無関係な数学的コードの拒否を確認するテストとフィクスチャを末尾に追加。既存テスト・import は変更しない。
- 新規 `phase171_closeout_r2r1_committed_head_guard/install.py`, `run.ps1`：内容ハッシュ検査、更新、限定テスト・文書生成、失敗時復元。

## 不変条件

1. `develop`、`HEAD == origin/develop`、Stage 変更なし。
2. R2 が審査した旧コミットからの祖先関係を確認し、後続コミットによる変更は R1/R1R1 監査パッケージと R3Z テストのみに制限する。
3. 5文書の `HEAD:path` Git blob は旧審査値と一致。R1R1 テストのコミット済み blob は旧版または審査済み新版の2状態のみ許可。作業ツリー側は審査済み修正内容のみ許可。
4. 既存の5文書・追記本文・テスト実行対象は R2 から変更しない。ドキュメントの全文出力と履歴保全を維持する。
5. 変更した2つの監査コードと5文書をバックアップし、失敗時には元に戻す。

## テスト・終了条件

作成環境では文書生成テスト13 PASS（新規2テストを含む）。Windows 実行では R2 の限定 pytest（文書更新テスト、Phase 170 文書契約、Phase 169 R3Z、R20R13R2）を実行し、結果は監査 JSON に記録する。全体 pytest は実行しない。

R2 成功時も Phase 171 は正式終了ではない。Phase 最終 Gate で現行アクティブ `tests/` の全体 pytest を一度だけ実行し、終了条件を評価する。表示冗長性の改善は Phase 172 以降に分離する。
