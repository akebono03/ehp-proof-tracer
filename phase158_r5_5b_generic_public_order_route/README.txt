Phase 158-R5-5b — generic public ordering route

目的
----
R5-5a repair3b で、pi_7^4 と pi_15^8 は proof graph / semantic block /
Argument の順序が正しく、public renderer route だけが逆転させていることを確認した。

実装方針
--------
group n/k の個別追加ではなく、

「depth >= 2 で、root conclusion を支える structured Narrative Argument が存在する」

という構造条件を generic public route の eligibility に使う。

既存 pi_8^5 dedicated route は今回の Phase boundary として維持する。

pi_15^8 の旧 dedicated renderer は、structured root Argument が使える場合は
generic route に譲る。

変更ファイル
------------
Production:
- toda_group_proof_narrative_renderer.py

Tests:
- tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
- tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py
- tests/test_phase158_r5_5b_public_generic_order_route.py

import 変更
-----------
なし。

完了条件
--------
1. pi_7^4 public depth=2 で nu4 decomposition premise が final group conclusion より前。
2. pi_15^8 public depth=2 で transported decomposition が final group conclusion より前。
3. pi_15^8 depth=2 で legacy dedicated renderer を呼ばない。
4. pi_8^5 の既存 dedicated route は維持。
5. pi_10^4 / pi_12^5 / pi_16^9 の既存 generic route contract を壊さない。
6. production change は renderer route のみ。
7. full repository pytest は実行しない。

次 Phase 境界
-------------
R5-5b では ordering route の接続のみ。

prose specificity、Reference 文面、全群 cutover、stable 判定などは先取りしない。
