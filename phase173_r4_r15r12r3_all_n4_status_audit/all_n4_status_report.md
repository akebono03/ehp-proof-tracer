# Phase 173 / n=4 全件・読み取り専用監査

- GitHub develop HEAD: `715dff58df263c419cdcb45c51a1fa169a87de45`
- 対象: `sphere.csv` の n=4, k=1..33 の全33群
- 方法: 実際の Proof Search と公開 Web model 経路を個別照合
- 全体 pytest: 未実施。本番コード変更: なし。
- `NAMED_COMPLETE`: 検索結果と検証済み公開 Web の双方が完成
- `ABSTRACT_ONLY_NAMED_PENDING`: 抽象群証明あり、記名生成元は未完成
- `NAMED_PENDING_NO_ABSTRACT`: 記名証明未完成、抽象群の証明も確認できない
- `NOT_VERIFIED_ERROR`: 実行例外等により確定できない（未完成と断定しない）

## k>=8 の集計

- `ABSTRACT_ONLY_NAMED_PENDING`: 26群

## 全33群

| k | 群 | DB位数 | 判定 | 未解決 Goal | 抽象群 | 出典/表示エラー |
|---:|---|---|---|---:|---|---|
| 1 | pi_5^4 | Z/2 | NAMED_COMPLETE | 0 | `-` | - |
| 2 | pi_6^4 | Z/2 | NAMED_COMPLETE | 0 | `-` | - |
| 3 | pi_7^4 | Z + Z/4 | NAMED_COMPLETE | 0 | `-` | - |
| 4 | pi_8^4 | Z/2 + Z/2 | NAMED_COMPLETE | 0 | `-` | - |
| 5 | pi_9^4 | Z/2 + Z/2 | NAMED_COMPLETE | 0 | `-` | - |
| 6 | pi_10^4 | Z/8 | NAMED_COMPLETE | 0 | `-` | - |
| 7 | pi_11^4 | 0 | NAMED_COMPLETE | 0 | `-` | - |
| 8 | pi_12^4 | Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 3 | `\mathbb{Z}/2` | - |
| 9 | pi_13^4 | Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{3}` | - |
| 10 | pi_14^4 | Z/8 + Z/4 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\mathbb{Z}/2 \oplus \mathbb{Z}/4 \oplus \mathbb{Z}/8` | - |
| 11 | pi_15^4 | Z/2 + Z/2 + Z/2 + Z/4 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{5} \oplus \mathbb{Z}/4` | - |
| 12 | pi_16^4 | Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{6}` | - |
| 13 | pi_17^4 | Z/8 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{2} \oplus \mathbb{Z}/8` | - |
| 14 | pi_18^4 | Z/2 + Z/8 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{2} \oplus \mathbb{Z}/8` | - |
| 15 | pi_19^4 | Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 3 | `\mathbb{Z}/2` | - |
| 16 | pi_20^4 | Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{3}` | - |
| 17 | pi_21^4 | Z/8 + Z/4 + Z/4 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{2} \oplus \left(\mathbb{Z}/4\right)^{2} \oplus \mathbb{Z}/8` | - |
| 18 | pi_22^4 | Z/8 + Z/2 + Z/2 + Z/2 + Z/4 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{5} \oplus \mathbb{Z}/4 \oplus \mathbb{Z}/8` | - |
| 19 | pi_23^4 | Z/2 + Z/2 + Z/2 + Z/2 + Z/4 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{5} \oplus \mathbb{Z}/4` | - |
| 20 | pi_24^4 | Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{6}` | - |
| 21 | pi_25^4 | Z/2 + Z/8 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{2} \oplus \mathbb{Z}/8` | - |
| 22 | pi_26^4 | Z/2 + Z/8 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{2} \oplus \mathbb{Z}/8` | - |
| 23 | pi_27^4 | Z/4 + Z/8 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\mathbb{Z}/4 \oplus \mathbb{Z}/8` | - |
| 24 | pi_28^4 | Z/2 + Z/2 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{5}` | - |
| 25 | pi_29^4 | Z/8 + Z/2 + Z/2 + Z/2 + Z/4 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{6} \oplus \mathbb{Z}/4 \oplus \mathbb{Z}/8` | - |
| 26 | pi_30^4 | Z/8 + Z/8 + Z/2 + Z/2 + Z/2 + Z/2 + Z/4 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{7} \oplus \mathbb{Z}/4 \oplus \left(\mathbb{Z}/8\right)^{2}` | - |
| 27 | pi_31^4 | Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/4 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{10} \oplus \mathbb{Z}/4` | - |
| 28 | pi_32^4 | Z/8 + Z/4 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{7} \oplus \mathbb{Z}/4 \oplus \mathbb{Z}/8` | - |
| 29 | pi_33^4 | Z/2 + Z/2 + Z/2 + Z/8 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{9} \oplus \mathbb{Z}/8` | - |
| 30 | pi_34^4 | Z/8 + Z/8 + Z/2 + Z/4 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{2} \oplus \mathbb{Z}/4 \oplus \left(\mathbb{Z}/8\right)^{2}` | - |
| 31 | pi_35^4 | Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{8}` | - |
| 32 | pi_36^4 | Z/8 + Z/2 + Z/2 + Z/2 + Z/2 + Z/2 + Z/4 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{6} \oplus \mathbb{Z}/4 \oplus \mathbb{Z}/8` | - |
| 33 | pi_37^4 | Z/8 + Z/2 + Z/2 + Z/8 + Z/2 + Z/2 + Z/2 + Z/2 | ABSTRACT_ONLY_NAMED_PENDING | 2 | `\left(\mathbb{Z}/2\right)^{6} \oplus \left(\mathbb{Z}/8\right)^{2}` | - |

## 未解決 Goal と表示診断

### k=8 / pi_12^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `CyclicStructureStatement, Relation, Relation`
- 表示不対応数式行: `1`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=12, sphere_dimension=4), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='ε₄', dimension=4, source=12, target=4, generator=GeneratorSymbol(family='\\varepsilon', index=4, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 0`

### k=9 / pi_13^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=13, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name='ν₇', dimension=7, source=10, target=7, generator=GeneratorSymbol(family='ν', index=7, decoration=None)), right=HomotopyElement(name='ν₁₀', dimension=10, source=13, target=10, generator=GeneratorSymbol(family='ν', index=10, decoration=None))))), FiniteCyclicGroup(order=2, generator=HomotopyElement(name='μ₄', dimension=4, source= [truncated]`

### k=10 / pi_14^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=14, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)))), FiniteCyclicGroup(order=4, generator=IteratedSuspension(expression=HomotopyElement(name="ε'", dimension=3, source=13, target=3, generator=GeneratorSymbol(family="\\varepsilon'", index=None, decoration=None)), exponent=1)), Finite [truncated]`

### k=11 / pi_15^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=15, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=HomotopyElement(name='η₁₄', dimension=14, source=15, target=14, generator=GeneratorSymbol(family='η', index=14, decoration=None))))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name [truncated]`

### k=12 / pi_16^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=16, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=Composition(left=HomotopyElement(name='η₁₄', dimension=14, source=15, target=14, generator=GeneratorSymbol(family='η', index=14, decoration=None)), right=HomotopyElement(name='η₁₅', dimension=15, source=16, t [truncated]`

### k=13 / pi_17^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=17, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name='ν₇', dimension=7, source=10, target=7, generator=GeneratorSymbol(family='ν', index=7, decoration=None)), right=HomotopyElement(name='σ₁₀', dimension=10, source=17, target=10, generator=GeneratorSymbol(family='σ', index=10, decoration=None))))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dim [truncated]`

### k=14 / pi_18^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=18, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ε₄', dimension=4, source=12, target=4, generator=GeneratorSymbol(family='\\varepsilon', index=4, decoration=None)), right=Composition(left=HomotopyElement(name='ν₁₂', dimension=12, source=15, target=12, generator=GeneratorSymbol(family='ν', index=12, decoration=None)), right=HomotopyElement(name='ν₁₅', dimension=15, source=18, target=15, generator=GeneratorSymbol(family='ν', index=15, decoration=None))))), FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElemen [truncated]`

### k=15 / pi_19^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `CyclicStructureStatement, Relation, Relation`
- 表示不対応数式行: `1`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=19, sphere_dimension=4), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='ε̅₄', dimension=4, source=19, target=4, generator=GeneratorSymbol(family='\\bar{\\varepsilon}', index=4, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 0`

### k=16 / pi_20^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=20, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name='ν₇', dimension=7, source=10, target=7, generator=GeneratorSymbol(family='ν', index=7, decoration=None)), right=Composition(left=HomotopyElement(name='σ₁₀', dimension=10, source=17, target=10, generator=GeneratorSymbol(family='σ', index=10, decoration=None)), right=HomotopyElement(name='ν₁₇', dimension=17, source=20, target=17,  [truncated]`

### k=17 / pi_21^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=21, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=HomotopyElement(name='σ₁₄', dimension=14, source=21, target=14, generator=GeneratorSymbol(family='σ', index=14, decoration=None))))), FiniteCyclicGroup(order=4, generator=Composition(left=HomotopyElement(name [truncated]`

### k=18 / pi_22^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=22, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=HomotopyElement(name="ρ''", dimension=7, source=22, target=7, generator=GeneratorSymbol(family="\\rho''", index=None, decoration=None)))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", [truncated]`

### k=19 / pi_23^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=23, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=HomotopyElement(name='μ₁₄', dimension=14, source=23, target=14, generator=GeneratorSymbol(family='\\mu', index=14, decoration=None))))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(n [truncated]`

### k=20 / pi_24^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=24, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=IteratedSuspension(expression=HomotopyElement(name="ν'", dimension=3, source=6, target=3, generator=GeneratorSymbol(family="\\nu'", index=None, decoration=None)), exponent=1), right=HomotopyElement(name='μ̅₇', dimension=7, source=24, target=7, generator=GeneratorSymbol(family='\\bar{\\mu}', index=7, decoration=None)))), FiniteCyclicGroup(order=2, generator=Composition(left=IteratedSuspension(expression=HomotopyElement(name="ν'", dimension=3, source=6, target=3, generator=GeneratorSymbol(family=" [truncated]`

### k=21 / pi_25^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=25, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=IteratedSuspension(expression=HomotopyElement(name="ν'", dimension=3, source=6, target=3, generator=GeneratorSymbol(family="\\nu'", index=None, decoration=None)), exponent=1), right=Composition(left=HomotopyElement(name='η₇', dimension=7, source=8, target=7, generator=GeneratorSymbol(family='η', index=7, decoration=None)), right=HomotopyElement(name='μ̅₈', dimension=8, source=25, target=8, generator=GeneratorSymbol(family='\\bar{\\mu}', index=8, decoration=None))))), FiniteCyclicGroup(order=8, g [truncated]`

### k=22 / pi_26^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=26, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ε₄', dimension=4, source=12, target=4, generator=GeneratorSymbol(family='\\varepsilon', index=4, decoration=None)), right=HomotopyElement(name='κ₁₂', dimension=12, source=26, target=12, generator=GeneratorSymbol(family='\\kappa', index=12, decoration=None)))), FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=HomotopyElement(name='ζ̅₇', dim [truncated]`

### k=23 / pi_27^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=27, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=4, generator=IteratedSuspension(expression=HomotopyElement(name='α̅', dimension=3, source=26, target=3, generator=GeneratorSymbol(family='\\bar{\\alpha}', index=None, decoration=None)), exponent=1)), FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=HomotopyElement(name='κ̅₇', dimension=7, source=27, target=7, generator=GeneratorSymbol(family='\\bar{\\kappa}', index=7, decoration=None)))))), [truncated]`

### k=24 / pi_28^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=28, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=HomotopyElement(name='δ₄', dimension=4, source=28, target=4, generator=GeneratorSymbol(family='\\delta', index=4, decoration=None))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='μ̅₄', dimension=4, source=21, target=4, generator=GeneratorSymbol(family='\\bar{\\mu}', index=4, decoration=None)), right=HomotopyElement(name='σ₂₁', dimension=21, source=28, target=21, generator=GeneratorSymbol(family='σ', index=21, decoration=None)))), FiniteCyclicGroup(order=2, generator=Composition(lef [truncated]`

### k=25 / pi_29^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=29, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=HomotopyElement(name='ρ₁₄', dimension=14, source=29, target=14, generator=GeneratorSymbol(family='\\rho', index=14, decoration=None))))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement( [truncated]`

### k=26 / pi_30^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=30, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name='ν₇', dimension=7, source=10, target=7, generator=GeneratorSymbol(family='ν', index=7, decoration=None)), right=HomotopyElement(name='κ̅₁₀', dimension=10, source=30, target=10, generator=GeneratorSymbol(family='\\bar{\\kappa}', index=10, decoration=None))))), FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement( [truncated]`

### k=27 / pi_31^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=31, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=Composition(left=HomotopyElement(name='ω₁₄', dimension=14, source=30, target=14, generator=GeneratorSymbol(family='\\omega', index=14, decoration=None)), right=HomotopyElement(name='η₃₀', dimension=30, source [truncated]`

### k=28 / pi_32^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=32, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=HomotopyElement(name="φ'''", dimension=7, source=32, target=7, generator=GeneratorSymbol(family="\\phi'''", index=None, decoration=None)))), FiniteCyclicGroup(order=4, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=IteratedSuspension(expression=HomotopyEle [truncated]`

### k=29 / pi_33^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=33, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=Composition(left=HomotopyElement(name='ω₁₄', dimension=14, source=30, target=14, generator=GeneratorSymbol(family='\\omega', index=14, decoration=None)), right=HomotopyElement(name='ν₃₀', dimension=30, source [truncated]`

### k=30 / pi_34^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=34, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=HomotopyElement(name='κ̅₁₄', dimension=14, source=34, target=14, generator=GeneratorSymbol(family='\\bar{\\kappa}', index=14, decoration=None))))), FiniteCyclicGroup(order=8, generator=Composition(left=Homoto [truncated]`

### k=31 / pi_35^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=35, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="φ'''", dimension=7, source=32, target=7, generator=GeneratorSymbol(family="\\phi'''", index=None, decoration=None)), right=HomotopyElement(name='ν₃₂', dimension=32, source=35, target=32, generator=GeneratorSymbol(family='ν', index=32, decoration=None))))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(na [truncated]`

### k=32 / pi_36^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=36, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=HomotopyElement(name="δ''", dimension=7, source=36, target=7, generator=GeneratorSymbol(family="\\delta''", index=None, decoration=None)))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ' [truncated]`

### k=33 / pi_37^4
- 抽象群必要条件: `True`、記名生成元の形状必要条件: `False`、前提診断: `NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED`
- 探索状態: `search_failed`、ProofStep: `0`
- 未解決 Goal 型: `Relation, Relation`
- 表示不対応数式行: `0`、生の Relation 診断行: `1`
- 診断: `expected a verified registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=37, sphere_dimension=4), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=8, generator=Composition(left=HomotopyElement(name='ν₄', dimension=4, source=7, target=4, generator=GeneratorSymbol(family='ν', index=4, decoration=None)), right=Composition(left=HomotopyElement(name="σ'", dimension=7, source=14, target=7, generator=GeneratorSymbol(family="\\sigma'", index=None, decoration=None)), right=HomotopyElement(name='ρ̅₁₄', dimension=14, source=37, target=14, generator=GeneratorSymbol(family='\\bar{\\rho}', index=14, decoration=None))))), FiniteCyclicGroup(order=2, generator=Composition(left=Homotopy [truncated]`
