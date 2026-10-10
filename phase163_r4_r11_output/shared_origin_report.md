# Phase 163 R4-R11 repair2 — 共通祖先の同一性診断

監査状態: **BLOCKED_BY_PROVENANCE**

欠落ノードへの到達回数: **14**

異なる Python オブジェクトとしての欠落ノード数: **2**

| ID | 関連成分 | Statement 型 | 推論規則名 | 前提数 | 不備 |
|---|---|---|---|---:|---|
| 1 | pi6_3_group_relation, pi7_4_group_relation, pi8_5_group_relation, higher_nu_group_relation | `Relation` | `Toda Prop.2.2 right formula` | 0 | `INFERENCE_PREMISES_MISSING` |
| 2 | pi8_5_group_relation, higher_nu_group_relation | `Relation` | `nested integer multiple` | 0 | `INFERENCE_PREMISES_MISSING` |

## 欠落ノード 1

- Statement: `Relation(lhs=MapApplication(map=MapSymbol(name='H'), expression=Composition(left=HomotopyElement(name='ν′', dimension=3, source=6, target=3, generator=GeneratorSymbol(family='ν', index=None, decoration='′')), right=Suspension(expression=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None))))), rhs=Composition(left=MapApplication(map=MapSymbol(name='H'), expression=HomotopyElement(name='ν′', dimension=3, source=6, target=3, generator=GeneratorSymbol(family='ν', index=None, decoration='′'))), right=Suspension(expression=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`
- note: `None`
- 到達経路:
  - `pi6_3_group_relation:root/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `pi6_3_group_relation:root/premise[3]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `pi7_4_group_relation:root/premise[1]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `pi7_4_group_relation:root/premise[1]/premise[3]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `pi8_5_group_relation:root/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `pi8_5_group_relation:root/premise[0]/premise[1]/premise[0]/premise[3]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `pi8_5_group_relation:root/premise[2]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `pi8_5_group_relation:root/premise[2]/premise[3]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `higher_nu_group_relation:root/premise[0]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `higher_nu_group_relation:root/premise[0]/premise[0]/premise[0]/premise[1]/premise[0]/premise[3]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `higher_nu_group_relation:root/premise[0]/premise[0]/premise[2]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]`
  - `higher_nu_group_relation:root/premise[0]/premise[0]/premise[2]/premise[3]/premise[0]/premise[0]/premise[0]/premise[3]`

## 欠落ノード 2

- Statement: `Relation(lhs=Multiple(coefficient=2, expression=Multiple(coefficient=2, expression=HomotopyElement(name='ν_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=3), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='ν', index=ScalarSymbol(name='n'), decoration=None)))), rhs=Multiple(coefficient=4, expression=HomotopyElement(name='ν_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=3), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='ν', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`
- note: `None`
- 到達経路:
  - `pi8_5_group_relation:root/premise[0]/premise[0]/premise[0]/premise[4]/premise[0]/premise[0]/premise[0]`
  - `higher_nu_group_relation:root/premise[0]/premise[0]/premise[0]/premise[0]/premise[0]/premise[4]/premise[0]/premise[0]/premise[0]`

未検証の成分は metadata_only を保持し、証明木や引用検証器は変更していません。
