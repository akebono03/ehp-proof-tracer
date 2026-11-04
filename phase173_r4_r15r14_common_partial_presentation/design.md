# R15R14：未完成証明の共通表示修正

## 対象

- `web_group_proof_common.py` の `_group_proof_statement_latex`。追加の import は関数内に限定する。
- `phase173_r4_r15r13_unified_presentation/layout.py` に `_public_search_diagnostic_line` を新規追加し、`canonicalize_proof_layout` から呼ぶ。
- `phase173_r4_r15r14_common_partial_presentation/tests/` に契約・結合テストを新規追加する。

## 方針

未証明の `CyclicStructureStatement` を新たに証明したとは扱わない。型が確定した場合に限り既存の公開用群構造 LaTeX Renderer に同等の記法で委譲する。モデルの `open_goals` と `diagnostics` は元のまま保持する。

公開 Web では `## 探索診断` 節に限り、既知の `expected a verified registered derivation for ..., found N` を検証済み導出候補数を保持した日本語に変える。未知の Python repr は一般的な案内に変えるが、認識できない通常の診断文は変更しない。内部データや監査ログには元の詳細を残す。

完成の Group proof・Reference・Citation・証明ステップと抽象群証明書には一切手を加えない。未完成の `generic-partial-proof` を `generic-complete-proof` に昇格させない。

## 完了条件

- `n=4,k=8,15` の未解決 CyclicStructureStatement が既存の目標と一致する数式表示になる。
- 公開診断に `Relation(lhs=...)` が露出しない。
- `n=4,k=8,15` は未完成、`n=4,k=4` は完成を維持。
- 限定 pytest PASS。全体 pytest は Phase 終了時のみ。

## 次工程との境界

Web の上段に出る `No proof-backed result found` と抽象群の表示関係、未完成証明書に対する Reference の列挙、一般の証明探索規則の追加は本修正の対象外。本文の構成やステータス判定の変更は行わない。
