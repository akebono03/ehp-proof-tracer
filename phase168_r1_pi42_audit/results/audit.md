# Phase 168 R1 — pi_4^2 現状監査

本監査は既存コード・DBを変更しない。

- Active status: `ProofSearchStatus.SEARCH_FAILED`
- Proven steps: `0`
- Open goals: `3`
- Root expansions: `3`
- Errors: `none`

## 次の調査対象

- `CyclicStructureStatement(group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2), generator=Composition(left=HomotopyElement(name='η₂', dimension=2, source=3, target=2, generator=GeneratorSymbol(family='η', index=2, decoration=None)), right=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), order=2)`
- `Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2), rhs=FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='η₂', dimension=2, source=3, target=2, generator=GeneratorSymbol(family='η', index=2, decoration=None)), right=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`
- `Relation(lhs=FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='η₂', dimension=2, source=3, target=2, generator=GeneratorSymbol(family='η', index=2, decoration=None)), right=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)))), rhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`

## 注意

Goal の取得や Reference の登録は証明完了を意味しない。
探索で未解決が残れば R2 の実装判断はその結果に基づいて行う。
