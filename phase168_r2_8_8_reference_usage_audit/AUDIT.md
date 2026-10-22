# Phase 168 R2-8⑧ 参照使用判定の監査

- 対象: π₄² の ProofStep → Replay → Presentation → Reference entries → Renderer。
- 既存コード変更なし。テストは限定3件のみ。
- `filter_toda_group_proof_narrative_reference_entries_by_step_usage()` は `id(proof_step)` が `used_step_ids` に含まれない項目を削除する。
- 現行 Narrative に `[R]` マーカーがない場合、共通 contribution renderer はステップ使用判定へ進む。
- この監査の `premise_used_entries` と `empty_used_entries` は比較用の仮定であり、Renderer 内部の実際の `generic_used_step_ids` ではない。
- 次の修正は、実際の使用ステップ ID とレンダリングされた本文に対応させた上で決定する。
