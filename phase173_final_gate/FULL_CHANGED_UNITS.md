# Phase 173 最終 Gate — 追加ファイル全文

今回の ZIP に含まれるファイルはすべて新規追加である。既存の import、クラス、関数、テストおよび正式文書は変更しない。

追加位置はリポジトリ直下の `phase173_final_gate/` とする。

- `phase173_final_gate/run.ps1`：省略のない PowerShell 実行スクリプト全文。
- `phase173_final_gate/gate.py`：import 全文、新規関数 `git()`、`validate_snapshot()`、`parse_pytest_summary()`、`write_report()`、`main()` の全文。
- `phase173_final_gate/tests/test_gate_contract.py`：import 全文、新規テスト関数5件の全文（パラメータを含む10ケース）。
- `phase173_final_gate/__init__.py`：新規モジュール。
- `phase173_final_gate/tests/__init__.py`：新規テストモジュール。
- `phase173_final_gate/README.md`：英語 README の全文。
- `phase173_final_gate/design.md`：日本語の設計記録全文。

各ファイルの全文を ZIP 内に個別保存している。コードの途中を `...` で省略しない。正式な `README.md` と `docs/` 配下の4文書は今回変更しない。Phase 173 の正式終了記録は、最終 Gate の全体 pytest 結果を得てから別工程で追記する。
