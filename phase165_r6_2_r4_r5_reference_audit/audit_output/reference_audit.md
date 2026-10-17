# π₄³ Reference 接続監査

- 登録命題: 201
- 型付き GIVEN と一致する命題: 17
- ルート逆向き候補: 3

## Proposition 5.1

- `shared:2:toda:adopted:prop5.1:finite_dimensional`：GIVEN=あり
  - `content.pi3_2_group_relation` (Relation)
  - `content.pi3_2_group_relation.lhs` (TodaPrimaryGroup)
  - `content.pi3_2_group_relation.rhs` (FreeCyclicGroup)
  - `content.pi3_2_group_relation.relation_type` (RelationType)
  - `content.pi3_2_group_relation.source` (NoneType)
  - `content.pi3_2_group_relation.note` (NoneType)
  - `content.eta2_hopf_relation` (Relation)
  - `content.eta2_hopf_relation.lhs` (MapApplication)
  - `content.eta2_hopf_relation.rhs` (HomotopyElement)
  - `content.eta2_hopf_relation.relation_type` (RelationType)
  - `content.eta2_hopf_relation.source` (NoneType)
  - `content.eta2_hopf_relation.note` (NoneType)
  - `content.delta_iota5_relation` (TodaDeltaImageUpToSignStatement)
  - `content.delta_iota5_relation.map` (TodaDeltaMap)
  - `content.delta_iota5_relation.element` (HomotopyElement)
  - `content.delta_iota5_relation.positive_value` (Multiple)
  - `content.higher_eta_group_relation` (Relation)
  - `content.higher_eta_group_relation.lhs` (TodaPrimaryGroup)
  - `content.higher_eta_group_relation.rhs` (FiniteCyclicGroup)
  - `content.higher_eta_group_relation.relation_type` (RelationType)
  - `content.higher_eta_group_relation.source` (NoneType)
  - `content.higher_eta_group_relation.note` (NoneType)
- `shared:2:toda:adopted:prop5.1:finite_dimensional:component:pi3_2_group_relation`：GIVEN=あり
  - `content.lhs` (TodaPrimaryGroup)
  - `content.lhs.group_dimension` (int)
  - `content.lhs.sphere_dimension` (int)
  - `content.rhs` (FreeCyclicGroup)
  - `content.rhs.generator` (HomotopyElement)
  - `content.relation_type` (RelationType)
  - `content.source` (NoneType)
  - `content.note` (NoneType)
- `shared:2:toda:adopted:prop5.1:finite_dimensional:component:eta2_hopf_relation`：GIVEN=あり
  - `content.lhs` (MapApplication)
  - `content.lhs.map` (MapSymbol)
  - `content.lhs.expression` (HomotopyElement)
  - `content.rhs` (HomotopyElement)
  - `content.rhs.name` (str)
  - `content.rhs.dimension` (int)
  - `content.rhs.source` (NoneType)
  - `content.rhs.target` (NoneType)
  - `content.rhs.generator` (GeneratorSymbol)
  - `content.relation_type` (RelationType)
  - `content.source` (NoneType)
  - `content.note` (NoneType)
- `shared:2:toda:adopted:prop5.1:finite_dimensional:component:delta_iota5_relation`：GIVEN=あり
  - `content.map` (TodaDeltaMap)
  - `content.map.source_group` (TodaPrimaryGroup)
  - `content.map.target_group` (TodaPrimaryGroup)
  - `content.element` (HomotopyElement)
  - `content.element.name` (str)
  - `content.element.dimension` (int)
  - `content.element.source` (NoneType)
  - `content.element.target` (NoneType)
  - `content.element.generator` (GeneratorSymbol)
  - `content.positive_value` (Multiple)
  - `content.positive_value.coefficient` (int)
  - `content.positive_value.expression` (HomotopyElement)
- `shared:2:toda:adopted:prop5.1:finite_dimensional:component:higher_eta_group_relation`：GIVEN=あり
  - `content.lhs` (TodaPrimaryGroup)
  - `content.lhs.group_dimension` (ScalarSum)
  - `content.lhs.sphere_dimension` (ScalarSymbol)
  - `content.rhs` (FiniteCyclicGroup)
  - `content.rhs.order` (int)
  - `content.rhs.generator` (HomotopyElement)
  - `content.relation_type` (RelationType)
  - `content.source` (NoneType)
  - `content.note` (NoneType)

## ルート候補

- Toda Proposition 5.1 generic higher-eta specialization
  - Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)
- generic cited typed scalar specialization
  - Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)
- equality symmetry
  - Relation(lhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), rhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)

## 注意
- 命題の登録と、探索への適用は別です。
- 未解決の前提を証明済みとは判定しません。
