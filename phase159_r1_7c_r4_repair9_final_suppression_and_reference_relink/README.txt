# Phase 159 R1-7c R4 repair9

## 目的

R4 closure 前に残った、次の2つの genuine regression を一般規則で修復する。

- R9-A: `pi_6^3` に再出現した reflexive equality
- R9-C: `pi_15^8` の public Reference と proof body marker の linkage 欠落

R9-B は production 修正対象にしない。
Equation (5.7) と Proposition 2.2 の dependency は既存 proof graph の契約として保持する。

## targeted audit で特定した落下箇所

### R9-A

`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`
では reflexive suppression の後に、

- visible relation ordering
- repeated unique-step suppression
- `insert_toda_group_proof_narrative_map_property_dependencies()`
- injective-image order reason ordering

が実行される。

このうち後段の dependency insertion によって、既に抑制した reflexive equality が再挿入され得る。
したがって、既存の
`suppress_toda_group_proof_narrative_reflexive_equalities()`
自体は変更せず、最後の dependency insertion 後に同じ一般規則を再適用する。

Phase 158 で確定した次の契約は変更しない。

- `eta_3 eta_4 eta_5 = eta_3^3` は distinct displayed equality なので保持
- `eta_3^3 = eta_3^3` は抑制
- `eta_5 = eta_5` は抑制

### R9-C

同じ renderer では、最初の
`link_toda_group_proof_narrative_unmarked_reference_consumers()`
の後に、

- body-usage filtering
- fixed Reference restoration
- step-usage filtering

が行われる。

したがって、最初の linkage pass の時点では存在しなかった、または後から復活した Reference が最終 Reference 集合に入る場合、
本文 marker を付ける機会がない。

修正は、最終 Reference 集合が決まった後、最後の body-usage filtering の直前に
`link_toda_group_proof_narrative_unmarked_reference_consumers()`
をもう一度適用する。

MAP_PROPERTY consumer を直接 literature Reference に帰属させない Phase 157 の規則は変更しない。

## production 変更対象

- `toda_group_proof_narrative_contribution_renderer.py`
  - `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

import 変更なし。
新規 production class / function なし。
群番号による special case 追加なし。

## tests

追加:

- `phase159_r1_7c_r4_repair9_final_suppression_and_reference_relink/test_phase159_r1_7c_r4_repair9.py`

確認:

- `pi_6^3` に `eta_5 = eta_5` が残らない
- canonical eta relation を壊さない
- `pi_15^8` の public Reference 全件が proof body に `[Rk]` linkage を持つ

既存 focused tests も実行する。

repository-wide pytest は実行しない。
Phase 159 の最後まで保留する。
