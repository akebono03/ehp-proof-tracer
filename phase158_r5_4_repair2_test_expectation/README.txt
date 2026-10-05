Phase 158-R5-4 repair2 — Test expectation correction
=====================================================

原因
----
repair1 で追加した test:
  test_phase158_r5_4_repair_pi6_3_keeps_existing_calculation_chain_numbering

は、pi_6^3 が repair 前に \tag{1} ... \tag{6} を持つと仮定していた。

しかし Phase 158-R5-4 の post-unification audit では、
repair 前の pi_6^3 は:
- left proof-item numbering: 0
- equation tags: 0
- tags without later reference: 0

であった。

したがって失敗は production repair の regression ではなく、
新規テストに入れた stale expectation である。

今回の変更
----------
Production code:
  変更なし

Test:
  tests/test_phase158_r5_4_repair_common_equation_numbering.py

修正内容:
- pi_6^3 固有の tag(1)..tag(6) 期待値を削除。
- pi_6^3 を共通 invariant test の対象へ追加。

共通 invariant
--------------
全対象群について:
1. 生成された \tag{N} の集合と、本文中で後続参照される (N) の集合が一致する。
2. 各 \tag{N} は対応する (N) より前に現れる。

これにより、特定群の過去の numbering 形を固定せず、
今回の Phase 158-R5-4 repair の一般規則だけを検証する。

Focused pytest
--------------
tests/test_phase158_r5_4_repair_common_equation_numbering.py
tests/test_phase144_5_generic_definition_order_equations.py
tests/test_phase144_5_r2_r2_api.py

その後、既存の R5-4 代表7群 audit を再実行する。

Full pytest
-----------
実行しない。Phase 158 closure のみ。
