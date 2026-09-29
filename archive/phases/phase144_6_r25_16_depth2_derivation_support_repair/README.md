# Phase 144-6 R25-16

## 変更対象

- `toda_group_proof_narrative_contribution_ordering.py`
  - 不採用となった R25-15 `_group_key` 変更を rollback。
- `toda_group_proof_narrative_argument_body_renderer.py`
  - `render_toda_group_proof_narrative_argument_body_markdown`
  - `direct_derivation_support_steps` と各 direct premise の既存 `premises`
    の関係を `step_derivation_sources_by_target_id` に補完。

## 目的

depth=2 semantic closure 後でも、ProofStep graph に存在する直接導出関係を
CALCULATION block の connector 生成へ渡す。

群・statement type・式文字列による special case は追加しない。

## テスト

- 新規 depth=2 connector regression
- R25-9b depth=2 definition
- pi6 generic production route
- Phase143 derivation connector / direct premise
- R25-9a hidden support

この段階では full pytest を実行しない。
