Phase 159 - pi_4^3 exactness reason unification repair2

目的
====
repair1 後の focused regression で、
tests/test_phase150_rc4_5c_2_exactness_to_map_property.py の
test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion()
だけが失敗した。

実際の現行出力:
  この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$.
  したがって,

古い Phase 150 期待値:
  この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.
  したがって,

Phase 159 の現行 prose と一致させるため、stale expectation のみ修正する。

変更対象
========
tests/test_phase150_rc4_5c_2_exactness_to_map_property.py

変更する関数
============
test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion()

import 変更
===========
なし。

実装変更
========
なし。

Phase 境界
==========
- EXACTNESS_TO_MAP_PROPERTY の実装は変更しない。
- EXACTNESS_TO_KERNEL の実装は変更しない。
- pi_4^3 固有処理は追加しない。
- equation numbering は変更しない。
- Reference は変更しない。
- repository-wide test は実行しない。

実行 pytest
===========
1. tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
2. tests/test_phase159_pi4_3_exactness_reason_unification.py
3. tests/test_phase50_pi4_3_exactness_bridge.py

完了条件
========
- Phase 150 exactness focused regression が PASS。
- Phase 159 exactness unification focused test が PASS。
- Phase 50 pi_4^3 exactness bridge が PASS。
