Phase157-R5-R6 repair2 — fixed component union selection

今回の5 failures の整理:

1. R2 statement_role 期待値
   - component が3件から4件になったのに role tuple が3件のままだった。
   - test expectation の更新漏れ。

2. bracket definition が Reference に出ない
   - 同一 Reference entry に複数 fixed components がある場合、
     selector は boundary-used candidate が1件でもあると、
     entry-external-used candidate を捨てていた。
   - bracket definition は proof-internal specialization を介して使われるため
     entry-external-used には入るが boundary-used には入らない。
   - 一般規則として両集合の union を candidate order で返す。

3. Lemma 5.2 / "$nu'$ を定める." が本文から消える
   - これは Phase156 の current public-boundary contract と一致。
   - (5.3) の内部導出を本文に展開しないのが現仕様。
   - R5-R6 と古い Phase144 tests の期待値を current contract に更新する。

変更対象:
- toda_group_proof_narrative_references.py
  - select_toda_group_proof_narrative_reference_statement_steps() 全体
- tests/test_phase157_r2_literature_statement_boundary.py
  - test_phase157_r2_equation53_inventory_has_no_group_order_policy() 全体
- tests/test_phase157_r5_r6_53_bracket_definition_reference.py
  - 全文
- tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py
  - 2 test functions

production imports:
- 変更なし

class:
- 変更なし

Phase boundary:
- Reference statement selection の一般規則だけ変更。
- Proof body ordering / prose は変更しない。
- 112群監査は focused PASS 後。
- repository-wide pytest は Phase157 closure のみ。
