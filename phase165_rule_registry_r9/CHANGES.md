# Phase 165 R9 変更一覧

- 新規 `audit.py`: `pattern_variables()`、`factory_inventory()`、`source_connections()`、`main()` を追加。既存コードは変更しない。
- 新規 `test_audit.py`: `test_factory_identifiers_are_unique()`、`test_audit_does_not_invoke_retired_catalog()` を追加。
- 新規 `run.ps1`: 監査と対象限定 pytest 2件のみ実行。
- 完了条件: R8 有効規則の ID 候補、重複候補、逆向きパターン適格性、接続元の監査レポート生成。
- 次 Phase 境界: Rule ID 永続化、台帳への正式登録、探索への移行は R10 以降。
- 全体 pytest は実施しない。
