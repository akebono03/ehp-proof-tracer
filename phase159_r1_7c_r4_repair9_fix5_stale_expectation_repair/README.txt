Phase 159 R1-7c R4 repair9 fix5

目的
====
R9-A stage audit により、

  2nu' = eta_3^3

は production pipeline の全 stage で存在し続けており、
最終本文にも

  [R2] より,
  2nu' = eta_3 eta_4 eta_5 = eta_3^3

として残っていることを確認した。

したがって fix4 の
`double_nu_prime=0`
は production defect ではなく、
単純形

  $2nu' = eta_3^3$

だけを完全一致で探した audit/test の stale expectation。

変更
====
Production:
- 変更なし

Test:
- tests/test_phase157_r20_repair30_final_reflexive_suppression.py
  - `test_phase157_r20_repair30_eta_bridge_and_hopf_support_remain()`

単純形または展開形のどちらでも
semantic relation が保持されていれば PASS とする。

R9-A 完了条件
=============
- literal `eta_5 = eta_5` が本文にない
- `2nu' = eta_3^3` の semantic relation が本文に残る
- Hopf support / eta bridge が残る

R9-C 完了条件
=============
- public Reference に orphan marker がない
- pi_15^8 transported relation が残る

Phase boundary
==============
- production は fix4 の状態を維持
- Equation (5.7) / Proposition 2.2 dependency は変更しない
- generator canonicalization は変更しない
- pi_4^3 はまだ見ない
- repository-wide pytest は実行しない
