Phase 159 - pi_4^3 repair3c fix7
Bounded upstream hop audit

背景
----
repair3c では provider anchor の upstream ancestry を local body 内で再帰的に
全展開した。その結果、代表6群の current contribution population が大幅に増加した。

Phase 144 R5-30 の既存設計では upstream attachment について、

- direct premise
- same Argument local body
- non-recursive single-hop

を境界としていた。

さらに audit 本文では、必要 fact を捕捉できない場合でも
「recursive に広げるのではなく rule を refine する」と明示されている。

目的
----
旧 downstream chain を基準として、upstream premise を

- 1 hop
- 2 hops
- 3 hops

だけ広げた場合の影響を比較する。

代表6群:
- added step count
- affected argument count
- block role 分布
- statement type 上位

pi_4^3:
必要4事実
- Delta(iota_5)=+-2 eta_2
- Im Delta
- ker E
- E surjective

が何 hop で初めて捕捉されるか確認する。

変更
----
Production code changes: NONE
Existing test changes: NONE
Document changes: NONE

pytest
------
- tests/test_phase144_6_r5_27_bounded_derivation_visibility_step_dedup_readiness_audit.py
- tests/test_phase144_6_r5_30_upstream_calculation_attachment_audit.py

repository-wide pytest は実行しない。

完了条件
--------
- pi_4^3 の4事実を捕捉する最小 hop depth が判明する。
- その hop depth の6群 impact が、unbounded repair3c より十分小さいか確認できる。
- historical non-recursive boundary をそのまま維持すべきか、
  semantic refinement が必要か判断できる。

この結果を見るまで production selection は変更しない。
