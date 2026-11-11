# Phase 174 R66 — テスト記録

- 作成環境：Python AST/compileall 構文検査 PASS。
- 分離環境で実行した R66 限定テスト：19 passed、Source Guard の実リポジトリ検査1件は deselected。
- GitHub `develop` の関連コード・テストを実装前に確認。
- Windows 上の Source Guard・公開証明の再実行・関連 pytest：未実施（ユーザーの実行ログで判定する）。
- 全体 pytest：未実施（Phase 174 最終段階まで延期）。

PowerShell `run.ps1` は `python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib` で R66/R65/R63 の限定テストを実行する。
