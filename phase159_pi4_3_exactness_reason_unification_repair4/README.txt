Phase 159 - pi_4^3 exactness reason unification repair4

目的
====
repair3 後、Phase 150 focused regression の同じ test function 内に
ローカル Phase 159 で追加された reason_body 検証が残っており、
そこだけ旧 prose expectation
  "$\ker E=\operatorname{Im}Δ=0$ である."
を保持していた。

現行出力は
  "$\ker E=\operatorname{Im}Δ=0$."
なので、この1行のみ修正する。

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

変更内容
========
変更前:
    "$\\ker E=\\operatorname{Im}Δ=0$ である."

変更後:
    "$\\ker E=\\operatorname{Im}Δ=0$."

実行 pytest
===========
1. tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
2. tests/test_phase159_pi4_3_exactness_reason_unification.py
3. tests/test_phase50_pi4_3_exactness_bridge.py

完了条件
========
上記3本がすべて PASS。

Phase 境界
==========
- EXACTNESS_TO_KERNEL 実装は変更しない。
- EXACTNESS_TO_MAP_PROPERTY 実装は変更しない。
- equation numbering は変更しない。
- Reference は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
