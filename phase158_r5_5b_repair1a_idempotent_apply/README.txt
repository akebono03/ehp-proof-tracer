Phase 158-R5-5b repair1a — idempotent apply

原因
----
repair1 の apply script は Production 側を先に書き換えたあと、
test helper `_web_text()` を exact string match で置換しようとした。

ユーザー環境ではその exact match が 0 件だったため、
apply script が途中終了した。

このため Production 修正は既に適用済みの可能性が高い。

今回の対応
----------
1. Production:
   - NEW_MERGE が既にあれば変更しない
   - OLD_MERGE があれば修正する
   - どちらも無ければ停止する

2. Test:
   - `_web_text()` を exact block match ではなく
     top-level function boundary で丸ごと置換する

変更対象
--------
Production:
- toda_group_proof_narrative_argument_multi_renderer.py
  - render_toda_group_proof_narrative_multi_argument_markdown()
  - 未適用の場合のみ変更

Test:
- tests/test_phase158_r5_5b_public_generic_order_route.py
  - _web_text()

import 変更
-----------
なし。

実行 pytest
-----------
1. tests/test_phase158_r5_5b_public_generic_order_route.py
2. tests/test_phase149_rc3_3_minimal_ordering.py
3. tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
4. tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py

repository-wide pytest は実行しない。

完了条件
--------
1. repair1a apply が途中停止しない。
2. Production の ordering repair が二重適用されない。
3. Web test が `## 証明` 以降だけを比較する。
4. pi_7^4 / pi_15^8 の proof body ordering が PASS。
5. Phase 149 ordering regression が PASS。
6. directly affected route-contract tests が PASS。
7. full repository pytest は Phase 158 の最後まで実行しない。
