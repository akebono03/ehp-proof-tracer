Phase 158-R5-5b repair1b — fix Web test literal

原因
----
repair1a の apply script が `_web_text()` を生成するとき、
置換文字列中の `"\n"` が test source 内の文字列リテラルではなく
実改行として展開された。

その結果 test file が、

return "
".join(...)

となり SyntaxError になった。

Production 状態
---------------
前回ログで:

Production local-body ordering repair: already applied

を確認済み。

したがって repair1b は Production code を変更しない。

変更対象
--------
Test only:

- tests/test_phase158_r5_5b_public_generic_order_route.py
  - `_web_text()` 全体

import 変更
-----------
なし。

修正方法
--------
`_web_text()` の完全な関数本文を `repr()` で apply script に埋め込み、
`\n` の escape を二重解釈させない。

実行 pytest
-----------
1. tests/test_phase158_r5_5b_public_generic_order_route.py
2. tests/test_phase149_rc3_3_minimal_ordering.py
3. tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
4. tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py

repository-wide pytest は実行しない。

完了条件
--------
1. test collection SyntaxError が消える。
2. R5-5b focused ordering tests が実行できる。
3. pi_7^4 / pi_15^8 proof-body ordering を確認できる。
4. Phase 149 ordering regression が PASS。
5. directly affected route-contract tests が PASS。
6. Production code を今回変更しない。
