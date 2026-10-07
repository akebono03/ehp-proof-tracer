Phase 159 exactness-reason stale expectation repair6

変更対象
========

test-only:

- tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
  - test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion()

- tests/test_phase157_r11_r17_residual_narrative_defects.py
  - test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use()

- tests/test_phase157_r20_repair43_dangling_connector_cleanup.py
  - test_phase157_r20_repair43_required_reason_sentences_remain()

production code:
- 変更なし

import:
- 変更なし

監査結果
========

ローカル current HEAD の reason renderer は
EXACTNESS_TO_MAP_PROPERTY を

  完全性より,
  $E: pi_5^2 -> pi_6^3$ は単射.

と描画する。

git diff は空であり、一時的な working-tree 変更ではない。

一方、上記3テストだけが旧契約

  この完全性と $Delta=0$ より,
  ker E = Im Delta = 0

を期待していた。

Phase 159 の簡潔な public prose 契約へ
テストを追随させる。

境界
====

- reason builder の semantic structure は変更しない。
- production renderer は変更しない。
- pi4_3 repair5 は変更しない。
- heavy Phase 144 cross-group fixture は実行しない。
- full test suite は Phase 159 終了時まで実行しない。
