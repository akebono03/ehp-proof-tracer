Phase 159 R1-7c R4 repair9 fix8

目的
====
fix7 の production 変更は正しいが、
fix7 package 内の新規 focused test が
Equation (5.7) の既存 classification を誤って
PROOF_INTERNAL と期待していた。

現行契約
========
Toda Equation 5.7 nu-prime eta_6 Hopf value は:

- classification: FIXED_STATEMENT
- reference locator: (5.7)
- component key: nu_prime_eta6_hopf_relation

GitHub の既存 Phase157-R5-R3 test も
この rule を fixed_statement としている。

変更
====
Production:
- なし

既存 repository tests:
- 変更なし

fix8 auxiliary focused test:
- 正しい FIXED_STATEMENT expectation に修正

検証
====
1. fix7 production syntax
2. corrected focused tests
3. existing boundary/inference tests
4. repair9 focused regressions
5. registration audit

全体 pytest は実行しない。
