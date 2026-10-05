Phase 158-R5-5b repair1d — root-only dependency-order preservation

診断結果
--------
R5-5b focused ordering tests:
5 passed.

pi_6^3 equation-numbering diagnosis:
- N1/N3 が同じ rendered equation に正規化される
- N4/N6 も同じ rendered equation に正規化される
- N2/N5 は reflexive equality として本文に出ない
- numbering 前の Markdown ですでに旧 calculation chain の表示形が失われている

したがって equation-numbering function 自体を変更するのではなく、
repair1 が変更した body ordering の適用範囲を狭める。

今回の一般則
------------
dependency-first local-body order を保持するのは、

argument.conclusion_block.role == TARGET

の Argument だけ。

Definition / Order など TARGET 以外の Argument は
既存の global block merge を維持する。

変更対象
--------
Production:
- toda_group_proof_narrative_argument_multi_renderer.py
  - render_toda_group_proof_narrative_multi_argument_markdown()

Tests:
- 変更なし

import:
- 変更なし

実行 pytest
-----------
1. tests/test_phase158_r5_5b_public_generic_order_route.py
2. tests/test_phase144_5_generic_definition_order_equations.py
3. tests/test_phase149_rc3_3_minimal_ordering.py
4. tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
5. tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py

repository-wide pytest:
実行しない。

完了条件
--------
1. R5-5b focused ordering 5件 PASS。
2. Phase 144 equation-numbering tests PASS。
3. Phase 149 local-body ordering regression PASS。
4. Phase 150 directly affected route tests PASS。
5. pi_7^4 / pi_15^8 は premise before target を維持。
6. pi_6^3 は既存 numbered calculation chain を維持。
7. full pytest は Phase 158 の最後まで実行しない。
