# Phase 165 R11 修正版

- `audit.py`: 新規 `resolved_rule_discovery_calls()` を `main()` の前に追加。`main()` 全体の監査で、文字列としての関数名チェックを廃止し、R8 からの import の別名と実際の呼び出しを検証する。
- `test_audit.py`: 修正先モジュールへの import を全文置換し、`test_r11_discovery_alias_resolution()` を追加。
- `run.ps1`: 修正監査と対象 pytest のみ実行。
- 本番コード変更なし、全体 pytest 未実施。
