# Phase 163 R4-R5 — 未対応 Toda 規則の構造的分類

生成関数・Statement 型・明示された文献参照を併記した候補監査であり、命題数の確定ではない。

## 件数

- rule_constructor_sites: 403
- toda_unmapped_sites: 277
- unlinked_boundary_components: 10

## 分類候補

- definition_candidate: 11
- explicit_reference_candidate: 3
- specialization_candidate: 30
- structured_rule_unresolved: 169
- unresolved_rule: 64

## 制限

- 規則名の definition / specialization は弱いヒントであり、数学的分類の確定ではない。
- `statement_type` は同一生成関数内で生成される型の候補であり、特定の規則との一致保証ではない。
- 文献参照 locator は直接的な AST 構築のみ抽出し、別変数・関数経由は未解決のまま残す。
- 旧 Registry・ProofStep・Renderer・Backward Search は変更しない。
- 引用可能性・数学的同一性・Definition の網羅性は未確認。
- 全体 pytest は未実施。
