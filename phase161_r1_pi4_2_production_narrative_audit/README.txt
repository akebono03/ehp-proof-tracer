Phase 161-R1
pi_4^2 production proof / public Narrative audit

目的
====
2-stem の unstable range の最初の対象 pi_4^2 について、
production proof と public Narrative を変更せずに監査する。

今回確認するもの
================
1. build_standard_toda_report(n=2, k=2) が選択する production result
2. TodaGroupResult.proof_step の root rule
3. root の direct premises
4. complete proof provenance
5. max_depth=2 の現在の public Narrative
6. (5.2), Proposition 4.4, eta_2 eta_3, QED の露出状況

既に GitHub 現行コードで確認した事項
==================================
- pi_4^2 の production construction は _build_pi4_2_step() を持つ。
- 結論は pi_4^2 = Z/2{eta_2 eta_3}。
- root は Toda (5.2) finite-cyclic transport に由来する。
- builder は pi_4^3 step と Toda (5.2) step を前提として inference する。
- 過去の literature-statement boundary audit では、
  この pi_4^2 finite-cyclic transport 自体は PROOF_INTERNAL と分類されている。

重要
====
この package は audit-only。
production source file は変更しない。
全体 pytest は実行しない。
Phase 161 の修正方針は、この監査出力を確認してから決める。

実行される focused tests
========================
tests/test_phase59_prop53_integration.py
tests/test_phase59_n3_ehp_chain.py
tests/test_phase160_generic_finite_cyclic_transport.py
tests/test_phase160_k2_generic_transport_connection.py

出力
====
output/phase161_r1_pi4_2_audit.txt
