# R10EH — 6/10/11/14-stem 表示・証明境界監査

AUDIT_ONLY。DB の表示名と文献に基づく証明を区別する。

| 群 | 探索 | 信頼境界 | 1段 E 等式 | 重複 | R10A | R10EC |
|---|---|---|---:|---:|---|---|
| pi_28^22 | complete | PASS | 17 | 0 | True | False |
| pi_32^22 | complete | PASS | 20 | 10 | False | False |
| pi_33^22 | partial | NOT_APPLICABLE_INCOMPLETE | — | — | — | — |
| pi_36^22 | partial | NOT_APPLICABLE_INCOMPLETE | — | — | — | — |

## pi_28^22

- 型付き Goal 候補: 1
- ProofStep: 54
- 生成元 ID と文献の区別: 4 / REVIEWED_GENERIC_FAMILY_SOURCE
- 生成元 ID と文献の区別: 4 / REVIEWED_GENERIC_FAMILY_SOURCE
- 完成本文: pi_28_22.md

## pi_32^22

- 型付き Goal 候補: 1
- ProofStep: 68
- 生成元 ID と文献の区別: 2 / LEGACY_ETA_DEFINITION_PATH
- 生成元 ID と文献の区別: 12 / REVIEWED_GENERIC_FAMILY_SOURCE
- 完成本文: pi_32_22.md

## pi_33^22

- 型付き Goal 候補: 1
- ProofStep: 3
- 生成元 ID と文献の区別: 16 / NO_REVIEWED_GENERIC_FAMILY_SOURCE_IN_THIS_REGISTRY
- 未解決型: CyclicStructureStatement
- 未解決型: GeneratorImage
- 未解決型: Relation
- 未解決型: Relation
- 探索診断: `expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=33, sphere_dimension=22), rhs=FiniteCyclicGroup(order=8, generator=HomotopyElement(name='ζ₂₂', dimension=22, source=33, target=22, generator=GeneratorSymbol(family='\\zeta', index=22, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 0`

## pi_36^22

- 型付き Goal 候補: 1
- ProofStep: 36
- 未解決型: GeneratorImage
- 未解決型: Relation
- 未解決型: Relation
- 探索診断: `expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=36, sphere_dimension=22), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='σ₂₂', dimension=22, source=29, target=22, generator=GeneratorSymbol(family='σ', index=22, decoration=None)), right=HomotopyElement(name='σ₂₉', dimension=29, source=36, target=29, generator=GeneratorSymbol(family='σ', index=29, decoration=None)))), FiniteCyclicGroup(order=2, generator`

## 次工程との境界

完成群については検証済み Proof Tree に基づく cyclic projection を別工程で検討する。
未完成群は不足する GeneratorImage と source-backed family definition の有無を監査し、
メタデータの存在だけで GIVEN を増やさない。
本監査は証明木、推論規則、文献、既存テスト、DB、本番 Renderer を変更しない。
全体 pytest は Phase 169 の終了時に実施する。
