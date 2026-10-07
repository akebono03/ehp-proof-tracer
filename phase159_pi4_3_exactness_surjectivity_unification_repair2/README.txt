Phase 159 - pi_4^3 exactness-to-surjectivity unification repair2

原因
====
public Narrative の connector normalization により、

  これより,

が reason paragraph の直前の standalone paragraph ではなく、

  これより, この完全性と ...

という同一 paragraph に結合される場合がある。

repair1 までの
_normalize_exactness_to_map_property_reason_prose()
は standalone の「これより,」だけを除去していたため、
このケースを正規化できなかった。

変更対象
========
toda_group_proof_narrative_reason_renderer.py

変更する関数
============
_normalize_exactness_to_map_property_reason_prose()

import 変更
===========
なし。

変更内容
========
reason paragraph を次の両方で認識する。

1. reason_body
2. "これより, " + reason_body

2 の場合は paragraph 自体を reason_body に置換する。
従来どおり、直前に standalone「これより,」がある場合も除去する。

pi_4^3 固有 hard-code は追加しない。

テスト変更
==========
なし。
既存の Phase 159 focused test がこの defect を直接検出しているため、
新規 test は追加しない。

実行 pytest
===========
1. tests/test_phase159_pi4_3_exactness_surjectivity_unification.py
2. tests/test_phase159_pi4_3_exactness_reason_unification.py
3. tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
4. tests/test_phase50_pi4_3_exactness_bridge.py

完了条件
========
- 「これより, この完全性と」が出ない。
- exactness-to-surjectivity reason body が1回表示される。
- surjective conclusion が reason より後に表示される。
- pi_4^3 kernel exactness を壊さない。
- pi_6^3 injective exactness を壊さない。
- Phase 50 bridge を壊さない。

Phase 境界
==========
- Reference selection は変更しない。
- equation numbering は変更しない。
- 他の reason kind は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
