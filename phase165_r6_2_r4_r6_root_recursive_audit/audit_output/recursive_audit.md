# π₄³ ルート候補の再帰展開監査

ルート候補: 3

## 候補 1: Toda Proposition 5.1 generic higher-eta specialization

- Subgoal: `Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`
- 深度 2: FORWARD_PASS（探索ノード 1）
  - `Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → FIXED_REFERENCE
- 深度 3: FORWARD_PASS（探索ノード 1）
  - `Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → FIXED_REFERENCE
- 深度 4: FORWARD_PASS（探索ノード 1）
  - `Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → FIXED_REFERENCE

## 候補 2: generic cited typed scalar specialization

- Subgoal: `Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`
- 深度 2: FORWARD_PASS（探索ノード 1）
  - `Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → FIXED_REFERENCE
- 深度 3: FORWARD_PASS（探索ノード 1）
  - `Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → FIXED_REFERENCE
- 深度 4: FORWARD_PASS（探索ノード 1）
  - `Relation(lhs=TodaPrimaryGroup(group_dimension=ScalarSum(left=ScalarSymbol(name='n'), right=1), sphere_dimension=ScalarSymbol(name='n')), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_n', dimension=ScalarSymbol(name='n'), source=ScalarSum(left=ScalarSymbol(name='n'), right=1), target=ScalarSymbol(name='n'), generator=GeneratorSymbol(family='η', index=ScalarSymbol(name='n'), decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → FIXED_REFERENCE

## 候補 3: equality symmetry

- Subgoal: `Relation(lhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), rhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`
- 深度 2: PREMISES_UNRESOLVED（探索ノード 2）
  - `Relation(lhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), rhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → NO_VERIFIED_DERIVATION
- 深度 3: PREMISES_UNRESOLVED（探索ノード 2）
  - `Relation(lhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), rhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → NO_VERIFIED_DERIVATION
- 深度 4: PREMISES_UNRESOLVED（探索ノード 2）
  - `Relation(lhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), rhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)` → NO_VERIFIED_DERIVATION

## 判定の限界
候補の存在は証明の完成を意味しません。
予算・深度の打ち切りは不可能性の証明ではありません。
