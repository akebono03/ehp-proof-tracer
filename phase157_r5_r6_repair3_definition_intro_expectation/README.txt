Phase157-R5-R6 repair3 — definition introduction expectation

今回の3 failures は test expectation の誤り。

現在の正しい挙動:
- [R1] (5.3) に bracket definition が表示される。
- Lemma 5.2 の内部導出説明は本文に出さない。
- ただし Narrative の definition introduction:
    まず, $\nu'$ を定める.
  は残す。

production code:
- 変更なし

変更対象:
- tests/test_phase157_r5_r6_53_bracket_definition_reference.py
- tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py

変更する test functions:
1. test_phase157_r5_r6_pi6_keeps_definition_intro_but_hides_lemma52_internal_derivation
2. test_phase144_6_r25_9b_depth2_narrative_has_definition
3. test_phase144_6_r25_9b_cli_depth2_narrative_has_definition

imports:
- 変更なし

完了条件:
- focused pytest が全件 PASS。
- bracket definition は Reference に表示。
- "$\nu'$ を定める." は本文に残る。
- "Lemma 5.2" は本文に出ない。

次:
- PASS 後に 112-group cross-audit 再実行。
- repository-wide pytest は Phase157 closure のみ。
