# 変更一覧

- `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` 内の `records.extend` 処理のみ修正。
- `MigrationRecord.assertion_id is None` の場合はそのレコードを変更せず保持。
- 識別子がある場合は従来どおり `shared:{index}:` 接頭辞を付与。
- 関数全体のコードは変更対象ファイルの既存本体を維持しているため、パッチは該当行だけの置換。インストーラーは変更前後を検証。
- 新規テスト: `test_unresolved_migration_record_without_assertion_id_is_retained()` と `test_nullable_migration_records_do_not_become_proof_links()`。
- 全体 pytest は Phase 165 終了時まで実施しない。
