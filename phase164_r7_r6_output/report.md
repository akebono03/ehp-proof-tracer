# Phase 164 R7-R6 最終監査（静的・読み取り専用）

- R7 完了判定: **静的監査だけでは認定しない**
- 既存本番コード変更: なし
- 全体 pytest: 未実施

## 標準入口

- generator: GUARD_CALL_PRESENT (find_standard_repository_generator_known_group_identity_nodes)
- operation: GUARD_CALL_PRESENT (query_standard_repository_operation_input)
- group: GUARD_CALL_PRESENT (build_standard_toda_report)

## 候補数

- 残存呼出候補: 33
- Registry・引用候補: 8
- `entries()` / `get()` / `build_repository_proof_scope()` は証明木用のため、それだけで違反ではない。

## 引用境界

- SOURCE_ARCHIVE: 検出
- PROOF_INTERNAL: 検出
- METADATA_ONLY: 検出
- verified_assertion_ids: 検出
- assess_citation: 検出

## 残件

- 静的に検出した Registry 直接参照は、数学的命題取得なのか検証・監査なのか個別に確認する。
- π₅³ の固定文献接続（原本確認経路）は R2 掲載順判定と同一ではない。
- ProofRepository の存在だけで出典・文献命題の真偽・引用適格性を認定しない。
- Source Archive、metadata_only は証明根拠への自動昇格を認めない。
- R7 終了には残件の用途分類・対象限定テスト・明示的完了判定が必要。

## 注意事項

これは AST による呼出候補検出であり、動的経路の全探索や数学的証明ではない。

