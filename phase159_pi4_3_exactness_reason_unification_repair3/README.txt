Phase 159 - pi_4^3 exactness reason unification repair3

目的
====
repair2 の apply script は Phase 150 test function 全体の完全一致を要求していた。
ローカル repository では Phase 159 の既存修正により関数本文に微差があり、
全文一致が 0 件となって適用できなかった。

repair3 は実装コードを変更せず、失敗ログで確認できた stale expectation の
1 行だけを置換する。

変更対象
========
tests/test_phase150_rc4_5c_2_exactness_to_map_property.py

変更する関数
============
test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion()

import 変更
===========
なし。

変更内容
========
変更前:
    "$\\ker E=\\operatorname{Im}Δ=0$ である.\n"

変更後:
    "$\\ker E=\\operatorname{Im}Δ=0$.\n"

実装ファイル
============
変更なし。

完了条件
========
- tests/test_phase150_rc4_5c_2_exactness_to_map_property.py が PASS。
- tests/test_phase159_pi4_3_exactness_reason_unification.py が PASS。
- tests/test_phase50_pi4_3_exactness_bridge.py が PASS。

Phase 境界
==========
- EXACTNESS_TO_KERNEL 実装は変更しない。
- EXACTNESS_TO_MAP_PROPERTY 実装は変更しない。
- equation numbering は変更しない。
- Reference は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
