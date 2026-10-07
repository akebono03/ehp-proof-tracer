Phase 159 R1-7c R3 repair4
==========================================

目的
----
R3 で本文は direct-premise specialization に整理されたが、
Reference は同じ literature step の aggregate statement 全体を表示していた。

pi_11^4 では次の余分な表示が残っていた。

Proposition 5.15:
- pi_9^2 = 0

Proposition 5.8:
- pi_6^2
- pi_7^3
- pi_8^4
- pi_9^5

repair4 では R3 の root-zero direct-premise plan を再利用し、
Reference も本文が実際に使う fixed component だけに絞る。

期待する Reference
------------------
[R1] Proposition 5.15.
pi_10^3 = 0.

[R2] Proposition 5.8.
pi_{n+4}^n = 0, n >= 6.

[R3] Proposition 4.4.
(alpha, beta) -> E alpha + nu_4 beta:
pi_{i-1}^3 + pi_i^7 -> pi_i^4 は同型.

変更対象
--------
Production:
- toda_group_proof_narrative_contribution_renderer.py

新規 tests:
- tests/test_phase159_r1_7c_r3_repair4_reference_component_pruning.py

新規 helper:
- _phase159_r1_7c_r3_repair4_aggregate_zero_component_line()
- prune_toda_group_proof_narrative_root_zero_direct_premise_references()

既存 function:
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
  - final Reference render の直前に repair4 pruning を1回追加するだけ。

Phase boundary
--------------
- Proof data は変更しない。
- Reference catalog は変更しない。
- Proposition 5.8 固有の locator/string 分岐は作らない。
- pi_11^4 固有の group branch は作らない。
- R3 structural plan に一致する root-zero direct-premise proof だけ適用。
- pi_6^3 など非該当 proof は no-op。
- repository-wide pytest は Phase159 最後まで実行しない。
