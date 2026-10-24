# Phase 168 R3-41G — 実探索での証明 Step 0件の原因監査

読み取り専用。登録済み命題・推論・ProofStep を変更せず観測する。

| 対象 | 状態 | 探索 Step | 採用イベント | 根の展開候補 | 展開呼出 | 未解決イベント | 分類 |
|---|---|---:|---:|---:|---:|---:|---|
| pi6_4 | search_failed | 0 | 0 | 3 | 4 | 5 | ROOT_EXPANSIONS_BUT_NO_ACCEPTED_PROOF_STEPS |
| pi6_3 | search_failed | 0 | 0 | 3 | 4 | 5 | ROOT_EXPANSIONS_BUT_NO_ACCEPTED_PROOF_STEPS |
| pi5_4_control | complete | 10 | 53 | 2 | 57 | 26 | COMPLETE_CONTROL |
| pi4_3_control | complete | 25 | 43 | 2 | 38 | 12 | COMPLETE_CONTROL |

## 判断の境界

- 完成例と未完成例で、探索候補と採用済み ProofStep の違いを調べる。
- 探索候補が存在することは、その前提の証明を意味しない。
- result.proven_steps にない証明を Renderer へ補充しない。
- Reference の欠落を証明できるのは、実際に引用付き ProofStep が存在する場合に限る。
- 詳細は audit.json の root_expansion_rules、first_expansions、unresolved_goals を確認する。
- 全体 pytest は Phase 終了時まで実施しない。
