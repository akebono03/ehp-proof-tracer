# Phase 165 R6-2 R2：引数必須規則の登録条件監査

- 状態: `AUDITED_READ_ONLY`
- 検出数: 22
- 本番コード変更: なし
- 証人の自動生成: なし

| Rule ID | 必須引数（型注釈） | 登録状態 |
|---|---|---|
| `homomorphism_rules.homomorphism_preserves_addition_inference_rule` | left: 型注釈なし, right: 型注釈なし | EXPLICIT_ONLY |
| `homomorphism_rules.homomorphism_preserves_inverse_inference_rule` | expression: 型注釈なし | EXPLICIT_ONLY |
| `homomorphism_rules.homomorphism_preserves_known_zero_inference_rule` | expression: 型注釈なし | EXPLICIT_ONLY |
| `homomorphism_rules.homomorphism_preserves_multiple_inference_rule` | coefficient: 型注釈なし, expression: 型注釈なし | EXPLICIT_ONLY |
| `homomorphism_rules.suspension_additivity_bridge_inference_rule` | left: 型注釈なし, right: 型注釈なし | EXPLICIT_ONLY |
| `homomorphism_rules.suspension_multiple_bridge_inference_rule` | coefficient: 型注釈なし, expression: 型注釈なし | EXPLICIT_ONLY |
| `hopf_rules.toda_prop22_left_inference_rule` | alpha: 型注釈なし, gamma: 型注釈なし | EXPLICIT_ONLY |
| `hopf_rules.toda_prop22_right_inference_rule` | alpha: 型注釈なし, gamma: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.additive_inverse_inference_rule` | expression: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.double_equals_repeated_sum_inference_rule` | expression: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.equality_preserved_under_left_composition_inference_rule` | left_expression: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.equality_preserved_under_multiple_inference_rule` | coefficient: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.equality_preserved_under_right_composition_inference_rule` | right_expression: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.iterated_suspension_one_bridge_inference_rule` | expression: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.nested_integer_multiple_inference_rule` | outer_coefficient: 型注釈なし, inner_coefficient: 型注釈なし, expression: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.sum_associativity_inference_rule` | left: 型注釈なし, middle: 型注釈なし, right: 型注釈なし | EXPLICIT_ONLY |
| `relation_rules.sum_commutativity_inference_rule` | left: 型注釈なし, right: 型注釈なし | EXPLICIT_ONLY |
| `scalar_rules.scalar_sign_evaluation_applies_to_multiple_inference_rule` | sign: 型注釈なし, expression: 型注釈なし | EXPLICIT_ONLY |
| `set_rules.equality_implies_modulo_inference_rule` | modulus: SubgroupTerm | EXPLICIT_ONLY |
| `set_rules.kernel_membership_implies_mapped_zero_inference_rule` | group_map: GroupMap, map_symbol: MapSymbol | EXPLICIT_ONLY |
| `set_rules.mapped_zero_implies_kernel_membership_inference_rule` | group_map: GroupMap, map_symbol: MapSymbol | EXPLICIT_ONLY |
| `set_rules.zero_implies_modulo_inference_rule` | modulus: SubgroupTerm | EXPLICIT_ONLY |

## 判定上の制約

- AST signatures do not verify runtime types or mathematical soundness.
- This audit does not call factories or manufacture typed witness arguments.
- A parameter annotation alone cannot establish a trusted source for its value.
- Only the nine R8 default modules are inventoried in this stage.

## 次 Phase との境界

R3 では個別 Provider と R8 外の一般規則を収集・整理する。R2 では規則本体も共通探索も変更しない。
