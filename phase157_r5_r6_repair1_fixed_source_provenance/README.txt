Phase157-R5-R6 repair1 — fixed source provenance

原因:
前回は Toda 5.3 nu-prime Lemma 5.2 bracket specialization を
FIXED_STATEMENT に変更した。

これは誤り。
specialization は Lemma 5.2 application のための PROOF_INTERNAL step であり、
文献 (5.3) の fixed statement 本体は、その premise の:

  ν' ∈ {η_3, 2ι_4, η_4}_1

である。

変更対象:
1. toda_upstream_bootstrap.py
   - proof import に InferenceRule, LiteratureReference を追加。
   - build_toda_53_nu_prime_steps() の bracket_membership_step に
     Toda (5.3) provenance を与える。

2. toda_literature_statement_boundary.py
   - nu_prime_bracket_definition component は維持。
   - bracket specialization の fixed mapping を削除。
   - specialization は既存 PROOF_INTERNAL classification に戻す。
   - source rule
     "Toda (5.3) nu-prime bracket definition"
     を nu_prime_bracket_definition に mapping。

3. tests/test_phase157_r2_literature_statement_boundary.py
   - (5.3) inventory test の期待値を3件から4件へ更新。
   - specialization is PROOF_INTERNAL test は変更しない。

4. tests/test_phase157_r5_r6_53_bracket_definition_reference.py
   - 全文再生成。
   - semantic closure の TodaBracketMembershipStatement 本体を検査。

renderer:
- 変更なし

Phase144 tests:
- 変更なし
- definition introduction が本文に残る既存契約をそのまま回帰確認する。

出力:
phase157_r5_r6_repair1_output/
- toda_upstream_bootstrap_import_after.txt
- build_toda_53_nu_prime_steps_after.txt

完了条件:
- (5.3) Reference に bracket definition が表示される。
- specialization は PROOF_INTERNAL。
- Lemma 5.2 application は本文に残る。
- 既存 Phase144 definition-introduction tests が PASS。
- focused tests all pass。

112群監査と repository-wide pytest はまだ実行しない。
