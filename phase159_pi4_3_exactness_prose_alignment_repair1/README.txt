Phase 159 - pi_4^3 exactness prose alignment repair1

原因
====
前パッケージの apply script が
def insert_toda_group_proof_narrative_reason_prose(
を探す際、実改行ではなく literal な "\n" を含む marker を使用していたため、
marker not found になった。

この失敗時点では対象実装ファイルはまだ write_text() されていないため、
実装変更は適用されていない。

変更対象
========
toda_group_proof_narrative_reason_renderer.py
tests/test_phase159_pi4_3_exactness_reason_unification.py

実装内容
========
前パッケージと同じ。

- EXACTNESS_TO_KERNEL の文末を
  「... である.」から「....」へ統一
- standalone 「これより,」と「完全性より,」の二重 connector を抑制
- exactness reason が包含済みの image/kernel standalone duplicate を抑制

pi_4^3 固有 hard-code は追加しない。

実行 pytest
===========
1. tests/test_phase159_pi4_3_exactness_reason_unification.py
2. tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
3. tests/test_phase50_pi4_3_exactness_bridge.py

全体テストは実行しない。
