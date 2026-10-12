# Phase 164 R7-R7 — 残存8箇所の用途分類

- 状態: **NOT_CLOSED**
- 本番ファイル変更: なし
- 全体 pytest: 未実行

## 監査対象8箇所

| ファイル | 呼出 | 分類 | 検出行 | 状態 |
|---|---|---|---|---|
| `phase164_r3_registry_search_connection.py` | `resolve_registered_statement` | shared_resolver_caller | 79 | PRESENT |
| `phase164_r4_r8_registry_reconstruction.py` | `assertion` | fixed_literature_special_path_exception | 104 | PRESENT |
| `phase164_r4_r8_registry_reconstruction.py` | `reference` | fixed_literature_special_path_exception | 105 | PRESENT |
| `phase163_source_archive_registry.py` | `reference` | source_archive_registration_only | 92 | PRESENT |
| `phase164_r7_repository_root_resolution.py` | `resolve_registered_statement` | shared_internal_root_caller | 27 | PRESENT |
| `phase164_r7_statement_resolution.py` | `assertion` | shared_resolver_implementation | 41 | PRESENT |
| `phase164_r7_statement_resolution.py` | `reference` | shared_resolver_implementation | 42 | PRESENT |
| `phase164_r7_statement_resolution.py` | `assess_phase164_r2_citation` | citation_policy_delegate | 80 | PRESENT |

## 3つの標準入口

- `find_standard_repository_generator_known_group_identity_nodes`: GUARDED
- `query_standard_repository_operation_input`: GUARDED
- `build_standard_toda_report`: GUARDED

## 完了を妨げる残件

- special_fixed_literature_path_not_migrated_to_shared_resolver

**判定:** π₅³ の固定文献接続には特殊な原本確認・ProofStep 同一性契約がある。共通 resolver の通常引用ポリシーとは同一視できない。R7-R8 で契約を明示して統合するまでは R7 全体を閉じない。

この監査は AST による存在確認であり、すべての動的経路の完全性を証明しない。
