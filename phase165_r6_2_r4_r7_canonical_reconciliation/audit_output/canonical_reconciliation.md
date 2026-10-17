# π₄³ 正規探索・ルート候補照合

Root Candidate 数: 3

| 経路 | 規則 | 正規探索 | ProofStep 観測 | 未解決 |
|---|---|---|---:|---:|
| ALL_ROOTS | 全候補 | UNRESOLVED_OR_AMBIGUOUS | 1 | 3 |
| ROOT_1 | Toda Proposition 5.1 generic higher-eta specialization | CANONICAL_COMPLETE | 2 | 0 |
| ROOT_2 | generic cited typed scalar specialization | CANONICAL_COMPLETE | 2 | 0 |
| ROOT_3 | equality symmetry | UNRESOLVED_OR_AMBIGUOUS | 0 | 3 |

## 正規探索の失敗情報

- ALL_ROOTS: `expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 2`
- ROOT_1: `None`
- ROOT_2: `None`
- ROOT_3: `expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 0`

## 限界
- `FORWARD_PASS` はこの監査の正規一意性判定とは別です。
- 各候補単独の実行でも、下位 Goal は元の共通 Provider を使います。
- 型付き Reference の厳格な一致を使い、未確認の文献を追加しません。
- 公開 Renderer はこの監査の対象外です。
