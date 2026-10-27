# Phase 169 R10EE — 1-stem 回帰監査

現行の探索結果を Phase 168 の固定基準と比較する読み取り専用監査。

| 群 | 現行状態 | ProofStep | Phase168 | Trust | 診断 |
|---|---|---:|---:|---|---|
| pi_3^2 | complete | 18 | 18 | PASS |  |
| pi_4^3 | complete | 25 | 25 | PASS |  |
| pi_5^4 | partial | 11 | 10 | NOT_APPLICABLE_INCOMPLETE | expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=4), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_4', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 2 |
| pi_6^5 | partial | 14 | — | NOT_APPLICABLE_INCOMPLETE | expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=6, sphere_dimension=5), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_5', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 2 |
| pi_10^8 | complete | 21 | — | PASS |  |

## 判定

**BLOCKED_ONE_STEM_REGRESSION**

`partial` を `complete` に読み替えない。候補数と診断から原因を特定するまで、
Phase 169 全体の終了を認定しない。

Proof Tree や引用命題の真偽をこの監査で新規証明しない。

全体 pytest は実施していない。
