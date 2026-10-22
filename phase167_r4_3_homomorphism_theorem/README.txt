# Phase 167 R4-③

目的: 公開 Narrative の商群同型の説明で、表示文言
`第一同型定理` を `準同型定理` に変更する。

## 変更対象

- `toda_group_proof_narrative_renderer.py`
- `render_toda_group_proof_narrative_markdown()`
  - 商群同型を挿入する文章1箇所のみ

## 非変更対象

- ProofStep
- 証明探索
- 命題台帳
- QuotientIsomorphismStatement
- 核・全射性・商群の導出
- Phase 167 R4-① の内部規則名非表示
- Phase 167 R4-② の型付き懸垂等式重複除去

## 実行

PowerShell で repository root から `run.ps1` を実行する。

全体 pytest は実行しない。
