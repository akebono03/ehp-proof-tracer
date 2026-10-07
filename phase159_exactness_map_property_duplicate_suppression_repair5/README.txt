Phase 159 - exactness map-property duplicate suppression repair5

前回 repair4 の状態
==================
production code の
suppress_toda_group_proof_narrative_repeated_unique_step_statements()
に "完全性より, " を追加する処理は成功した。

その後、pi_4^3 test への brittle な文字列置換が一致せず停止した。

今回の変更
==========
文字列 block の完全一致置換をやめ、
対象 test function を関数単位で置き換える。

変更対象
========
1. toda_group_proof_narrative_contribution_renderer.py
   - 前回適用済みなら変更なし
   - 未適用なら connector_prefixes に "完全性より, " を追加

2. tests/test_phase159_pi4_3_exactness_surjectivity_unification.py
   - test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector()
     を関数全体で置換
   - public Narrative 内の E 全射が1回だけであることを確認

3. tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
   - test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion()
     を関数全体で置換
   - public Narrative 内の E 単射が1回だけであることを確認

import 変更
===========
なし。

期待する public prose
=====================
pi_4^3:
  [R1]より, pi_4^5=0.
  完全性より, E:pi_3^2->pi_4^3 は全射.

pi_6^3:
  Delta=0.
  完全性より, E:pi_5^2->pi_6^3 は単射.

同じ map-property conclusion の standalone 再表示はしない。

Phase 境界
==========
- exactness reason builder は変更しない。
- exactness reason renderer は変更しない。
- Reference selection は変更しない。
- equation numbering は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
