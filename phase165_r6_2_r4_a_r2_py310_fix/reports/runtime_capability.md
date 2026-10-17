# Phase 165 R6-2 R4-A-R2 実行時収集監査

- 状態: `OK`
- 対象: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`

## 件数

| 指標 | 件数 |
|---|---:|
| R4-A AST 収集対象候補 | 55 |
| 実行時生成された規則 | 55 |
| 逆向きパターンの構造候補 | 25 |
| 具体 Goal に対する逆向き適用実証 | 0（未実施） |
| 完成証明の再構成実証 | 0（未実施） |

## R8 実行時規則（factory 名との直接対応は未確定）

| モジュール | 規則名 | 結論パターン | 前提数 | 逆向き構造候補 |
|---|---|---|---:|---|
| `ehp_rules` | `EHP exactness transfers image structure to kernel` | あり | 2 | 候補 |
| `ehp_rules` | `EHP exactness implies zero composition` | あり | 1 | 候補 |
| `ehp_rules` | `EHP exactness from image and kernel` | あり | 2 | 候補 |
| `ehp_rules` | `EHP exactness transfers kernel structure to image` | あり | 2 | 候補 |
| `ehp_rules` | `EHP zero composition implies zero relation` | あり | 1 | 候補 |
| `stable_rules` | `Freudenthal boundary range implies suspension epimorphism` | なし | 1 | 未確認 |
| `stable_rules` | `Freudenthal stable range implies suspension isomorphism` | なし | 1 | 未確認 |
| `stable_rules` | `Suspension injectivity reflects equality` | なし | 2 | 未確認 |
| `stable_rules` | `Suspension injectivity reflects zero` | なし | 2 | 未確認 |
| `stable_rules` | `Suspension isomorphism implies injectivity` | なし | 1 | 未確認 |
| `set_rules` | `coset equality implies modulo` | なし | 1 | 未確認 |
| `set_rules` | `difference membership implies modulo` | なし | 1 | 未確認 |
| `set_rules` | `exactness implies subgroup equality` | なし | 1 | 未確認 |
| `set_rules` | `membership subset propagation` | あり | 2 | 候補 |
| `set_rules` | `modulo implies coset equality` | あり | 1 | 候補 |
| `set_rules` | `modulo implies difference membership` | あり | 1 | 候補 |
| `set_rules` | `mutual subset implies subgroup equality` | あり | 2 | 候補 |
| `set_rules` | `subgroup equality implies subset` | あり | 1 | 候補 |
| `set_rules` | `subgroup equality membership propagation` | なし | 2 | 未確認 |
| `set_rules` | `subgroup equality modulo propagation` | なし | 2 | 未確認 |
| `set_rules` | `subgroup equality symmetry` | あり | 1 | 候補 |
| `set_rules` | `subgroup equality transitivity` | あり | 2 | 候補 |
| `set_rules` | `subset transitivity` | あり | 2 | 候補 |
| `hopf_rules` | `EHP H preserves equality` | なし | 1 | 未確認 |
| `hopf_rules` | `EHP E-H zero composition implies suspended Hopf zero` | なし | 2 | 未確認 |
| `hopf_rules` | `generalized Hopf composition formula` | なし | 2 | 未確認 |
| `hopf_rules` | `generalized Hopf invariant enables composition law` | なし | 1 | 未確認 |
| `hopf_rules` | `generalized Hopf invariant to EHP H equality` | なし | 1 | 未確認 |
| `hopf_rules` | `generalized Hopf invariant value is zero` | なし | 2 | 未確認 |
| `hopf_rules` | `generalized Hopf left composition formula` | なし | 1 | 未確認 |
| `hopf_rules` | `generalized Hopf invariant enables left composition law` | なし | 2 | 未確認 |
| `scalar_rules` | `Even exponent evaluates minus-one power to one` | なし | 1 | 未確認 |
| `scalar_rules` | `Even scalar implies congruence to zero modulo two` | なし | 1 | 未確認 |
| `scalar_rules` | `Scalar congruent to one modulo two preserves order-two element` | あり | 2 | 候補 |
| `scalar_rules` | `Odd exponent evaluates minus-one power to minus one` | なし | 1 | 未確認 |
| `scalar_rules` | `Odd scalar implies congruence to one modulo two` | なし | 1 | 未確認 |
| `relation_rules` | `composition equality to zero` | あり | 1 | 候補 |
| `relation_rules` | `equality symmetry` | あり | 1 | 候補 |
| `relation_rules` | `equality transitivity` | あり | 2 | 候補 |
| `relation_rules` | `order implies zero multiple` | あり | 1 | 候補 |
| `relation_rules` | `suspension composition functoriality` | なし | 1 | 未確認 |
| `relation_rules` | `suspension preserves equality` | あり | 1 | 候補 |
| `relation_rules` | `suspension preserves zero` | あり | 1 | 候補 |
| `relation_rules` | `suspension preserves zero multiple` | なし | 1 | 未確認 |
| `relation_rules` | `zero composition equality implies zero` | あり | 2 | 候補 |
| `relation_rules` | `zero composition reverse equality implies zero` | あり | 2 | 候補 |
| `relation_rules` | `zero equality implies zero` | あり | 2 | 候補 |
| `map_property_rules` | `injective map reflects equality` | なし | 2 | 未確認 |
| `map_property_rules` | `isomorphism implies injectivity` | なし | 1 | 未確認 |
| `homomorphism_rules` | `homomorphism preserves zero` | なし | 1 | 未確認 |
| `homomorphism_rules` | `suspension is homomorphism` | あり | 0 | 未確認 |
| `indeterminacy_rules` | `coset membership implies modulo` | なし | 1 | 未確認 |
| `indeterminacy_rules` | `equality implies sign indeterminacy` | あり | 1 | 候補 |
| `indeterminacy_rules` | `modulo implies coset membership` | あり | 1 | 候補 |
| `indeterminacy_rules` | `Symbolic odd equality implies coefficient indeterminacy` | なし | 2 | 未確認 |

## 除外 factory

- `set_rules.equality_implies_modulo_inference_rule:requires-input`
- `set_rules.kernel_membership_implies_mapped_zero_inference_rule:requires-input`
- `set_rules.mapped_zero_implies_kernel_membership_inference_rule:requires-input`
- `set_rules.zero_implies_modulo_inference_rule:requires-input`
- `hopf_rules.toda_prop22_left_inference_rule:requires-input`
- `hopf_rules.toda_prop22_right_inference_rule:requires-input`
- `scalar_rules.scalar_sign_evaluation_applies_to_multiple_inference_rule:requires-input`
- `relation_rules.additive_inverse_inference_rule:requires-input`
- `relation_rules.double_equals_repeated_sum_inference_rule:requires-input`
- `relation_rules.equality_preserved_under_left_composition_inference_rule:requires-input`
- `relation_rules.equality_preserved_under_multiple_inference_rule:requires-input`
- `relation_rules.equality_preserved_under_right_composition_inference_rule:requires-input`
- `relation_rules.iterated_suspension_one_bridge_inference_rule:requires-input`
- `relation_rules.nested_integer_multiple_inference_rule:requires-input`
- `relation_rules.sum_associativity_inference_rule:requires-input`
- `relation_rules.sum_commutativity_inference_rule:requires-input`
- `homomorphism_rules.homomorphism_preserves_addition_inference_rule:requires-input`
- `homomorphism_rules.homomorphism_preserves_inverse_inference_rule:requires-input`
- `homomorphism_rules.homomorphism_preserves_known_zero_inference_rule:requires-input`
- `homomorphism_rules.homomorphism_preserves_multiple_inference_rule:requires-input`
- `homomorphism_rules.suspension_additivity_bridge_inference_rule:requires-input`
- `homomorphism_rules.suspension_multiple_bridge_inference_rule:requires-input`

## 制約

- Importing existing production modules can execute their import-time code; probe itself performs no writes.
- PYTHONDONTWRITEBYTECODE prevents bytecode writes only, not side effects of imported project modules.
- Instantiated rules are not automatically backward applicable to concrete Goals.
- Static call edges do not certify runtime search reachability.
- No forward proof, mathematical soundness, Goal applicability, or passing existing test is inferred.
- Module-by-module R8 discovery may differ from default all-module discovery if modules have cross-import side effects.

## 次段階

R4-A-R3：source factory の実行時同定、具体的 Goal ごとの逆向き適用、探索到達性を証明成功と分離して検査する。
