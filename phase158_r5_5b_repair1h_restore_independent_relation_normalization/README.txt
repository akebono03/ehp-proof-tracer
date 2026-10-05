Phase 158-R5-5b repair1h — restore independent relation-side normalization

原因
----
Phase 157 の generic eta-family normalization 追加時に、
`_normalize_generic_narrative_statement_latex()` が statement 全体へ先に

_normalize_generic_eta_family_latex(latex)

を適用する構造になった。

このため Relation の元の lhs/rhs の文字列位置を探す前に、
eta-family の composition が canonical power form に潰れる。

例:

eta_3 eta_4 eta_5 = eta_3^3

が、

eta_3^3 = eta_3^3

へ変わる。

これは Phase 156 R6 repair2 の
「relation sides normalize independently」
という canonical contract の回帰。

修正方針
--------
lhs/rhs を持たない statement:
- 従来どおり statement 全体を eta-family normalization。

lhs/rhs を持つ statement:
- 元の latex 上で lhs/rhs の位置を独立に見つける。
- 各 expression の normalized rendering だけを置換する。
- 置換後に statement 全体を再 normalize しない。

これにより:
- distinct equality sides を保持
- order statement の lhs canonicalization は維持
- pi_6^3 numbered calculation chain を復元
- Phase 157 reflexive-equality suppression を維持
- group-specific rule を追加しない

変更対象
--------
Production:
- toda_group_proof_generic_narrative_renderer.py
  - _normalize_generic_narrative_statement_latex()

Tests:
- 新規・変更なし。
- 既存 canonical tests を回帰条件として使用。

import:
- 変更なし。

実行 pytest
-----------
1. tests/test_phase156_r6_repair2_independent_relation_side_normalization.py
2. tests/test_phase157_r20_repair28_match_step_level_eta_normalization.py
3. tests/test_phase149_rc3_3_minimal_ordering.py
4. tests/test_phase158_r5_5b_public_generic_order_route.py
5. tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
6. tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py

repository-wide pytest:
実行しない。

完了条件
--------
1. eta_3 eta_4 eta_5 = eta_3^3 が reflexive equality に潰れない。
2. pi_6^3 の numbered calculation chain が復元する。
3. Phase 157 の本当に reflexive な step は非表示のまま。
4. pi_7^4 / pi_15^8 の premise-before-target ordering を維持。
5. group-specific special case を追加しない。
6. full repository pytest は Phase 158 の最後まで実行しない。
