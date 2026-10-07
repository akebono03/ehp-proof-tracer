Phase 159 - exactness connector normalization repair3

原因
====
EXACTNESS_TO_MAP_PROPERTY の reason prose は
insert_toda_group_proof_narrative_reason_prose() 内では正規化できていた。

しかし public Narrative pipeline ではその後に

normalize_toda_group_proof_narrative_connectors()

が実行される。

この関数が standalone の

  これより,

を次の exactness reason paragraph に結合し、

  これより, この完全性と ...

を再生成していた。

変更対象
========
toda_group_proof_narrative_contribution_renderer.py

変更する関数
============
normalize_toda_group_proof_narrative_connectors()

import 変更
===========
なし。

一般規則
========
standalone connector が「これより,」で、
次段落が

- 「この完全性と ...」
- 「完全性より, ...」

で始まる場合、「これより,」を捨てる。

通常の

  これより, Im Delta = ...

などは従来どおり結合する。

pi_4^3、eta_2、特定の群・命題名は hard-code しない。

テスト
======
新規:
tests/test_phase159_exactness_connector_normalization.py

3件:
1. 「これより, この完全性と」を抑制
2. 通常の「これより」は維持
3. 「これより, 完全性より」を抑制

既存回帰:
- tests/test_phase159_pi4_3_exactness_surjectivity_unification.py
- tests/test_phase159_pi4_3_exactness_reason_unification.py
- tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
- tests/test_phase50_pi4_3_exactness_bridge.py

完了条件
========
上記すべて PASS。

Phase 境界
==========
- reason builder は変更しない。
- Reference selection は変更しない。
- equation numbering は変更しない。
- 群計算は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
