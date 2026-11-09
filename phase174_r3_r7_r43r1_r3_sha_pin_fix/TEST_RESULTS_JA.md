# R43R1 テスト結果

- GitHub の R3 EHP ファイルの正しい Git blob SHA 40桁を確認。
- `source_guard.py` の変更後内容は旧 SHA 35桁 → 新 SHA 40桁の1件のリテラル差し替えのみ。
- 既存の検証関数・検証分岐の AST が同一であることを契約テスト化。
- 本コンテナには Windows ユーザー側の Git 作業ツリーが存在しないため、Live Source Guard・R43 実監査は未実施。
- R43R1 限定 pytest `tests/test_fix.py`: 5 PASS（コンテナで実行）。
- `run.ps1` は R43R1 限定 pytest を行い、既存 R43 `run.ps1` の DryRun と通常実行を引き継ぐ。
- 全体 pytest は実施しない。
