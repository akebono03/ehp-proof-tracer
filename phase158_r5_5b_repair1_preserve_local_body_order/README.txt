Phase 158-R5-5b repair1 — preserve local body dependency order

原因
----
R5-5b の route cutover 後も pi_7^4 / pi_15^8 の本文順序が逆だった。

R5-5a で確認済み:
- proof graph は正しい
- semantic block dependency は正しい
- generic proof order は正しい
- Narrative Argument は正しい

現行 multi-Argument renderer を確認すると、

extract_toda_group_proof_narrative_argument_local_body_blocks(...)

は dependency-first で conclusion を最後に並べる。

しかし直後に、

local_body_blocks = tuple(
  block
  for block in blocks
  if ...
)

として global `blocks` order に並べ直している。

このため正しい local dependency order が失われていた。

この原因は Phase 149 RC3-3 repair の README にも同じ形で記録されている。

変更対象
--------
Production:
- toda_group_proof_narrative_argument_multi_renderer.py
  - render_toda_group_proof_narrative_multi_argument_markdown()

Test:
- tests/test_phase158_r5_5b_public_generic_order_route.py
  - _web_text()

import 変更
-----------
なし。

Production 修正
---------------
local_body_blocks の既存 dependency-first order を保持する。

method evidence のうち local body にまだ含まれていない block だけを、
argument conclusion block の直前へ追加する。

これにより:
- local dependency order を壊さない
- method evidence を失わない
- conclusion は support/evidence より後になる

Web test 修正
-------------
Web 全体の文字列には `## 証明対象` に final target が先に現れるため、
全体 `index()` 比較は ordering test として不正だった。

`## 証明` 以降の proof body のみを抽出して比較する。

実行 pytest
-----------
1. tests/test_phase158_r5_5b_public_generic_order_route.py
2. tests/test_phase149_rc3_3_minimal_ordering.py
3. tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
4. tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py

repository-wide pytest は実行しない。

完了条件
--------
1. pi_7^4 の proof body で nu4 decomposition が final group conclusion より前。
2. pi_15^8 の proof body で transported decomposition が final group conclusion より前。
3. Phase 149 の exactness ordering regression が PASS。
4. 既存 generic route contracts が PASS。
5. proof graph / semantic model / Argument ordering は変更しない。
6. full repository pytest は Phase 158 最後まで実行しない。

次 Phase 境界
-------------
R5-5b repair1 は ordering loss の修正のみ。

Reference 文面、prose specificity、pi_8^5 dedicated route の廃止、
stable 判定、全群 cutover は先取りしない。
