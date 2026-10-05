Phase 158-R5-5b repair1j — rendered reflexive equality suppression

原因
----
repair1i で canonical chain の欠落箇所を特定した。

Multi-Argument output:
- equation (1): present
- equation (2): missing
- connector "(1) と (2) より,": missing
- equation (3) tagged form: missing
- order statement: present

Phase 156 repair1h により、
generic step renderer 自体は

eta_3 eta_4 eta_5 = eta_3^3

を distinct equality として描画できる。

しかし Phase 157 の helper:

_is_toda_group_proof_narrative_rendered_reflexive_equality_step()

は lhs/rhs をさらに eta-family normalize して比較するため、

eta_3 eta_4 eta_5
and
eta_3^3

を同一と誤判定し、equation (2) を本文から suppression していた。

修正方針
--------
「rendered reflexive equality」は、
実際の public generic step rendering の左右が文字列として同一の場合だけ True とする。

例:

eta_3^3 = eta_3^3
-> suppress

eta_5 = eta_5
-> suppress

eta_3 eta_4 eta_5 = eta_3^3
-> keep

この判定は群番号に依存しない。

変更対象
--------
Production:
- toda_group_proof_narrative_argument_body_renderer.py
  - import block
  - _is_toda_group_proof_narrative_rendered_reflexive_equality_step()

削除 import:
- _normalize_generic_eta_family_latex
- _render_generic_narrative_expression_latex

Tests:
- 新規・変更なし。
- 既存 canonical tests をそのまま回帰条件に使用。

実行 pytest
-----------
1. tests/test_phase156_r6_repair2_independent_relation_side_normalization.py
2. tests/test_phase157_r20_repair28_match_step_level_eta_normalization.py
3. tests/test_phase149_rc3_3_minimal_ordering.py
4. tests/test_phase158_r5_5b_public_generic_order_route.py
5. Phase 150 directly affected route-contract tests

repository-wide pytest:
実行しない。

完了条件
--------
1. Phase 156 canonical chain (1),(2),(3) が復元する。
2. Phase 157 true rendered reflexive equalities は非表示のまま。
3. Phase 149 numbered calculation-chain contract が PASS。
4. pi_7^4 / pi_15^8 premise-before-target ordering が維持。
5. group-specific special case を追加しない。
6. full pytest は Phase 158 の最後まで実行しない。
