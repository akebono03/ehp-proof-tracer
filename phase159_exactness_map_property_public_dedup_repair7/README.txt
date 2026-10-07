Phase 159 - exactness map-property public dedup repair7

原因
====
unique-step dedup は presentation node の canonical rendering をキーにする。

canonical rendering:
  $E: ...$ は単射である.
  $E: ...$ は全射である.

現在の public exactness prose:
  完全性より, $E: ...$ は単射.
  完全性より, $E: ...$ は全射.

したがって、「完全性より,」を除去しても
「は単射である」と「は単射」、
「は全射である」と「は全射」
が異なるキーになり、重複を認識できなかった。

変更対象
========
1. toda_group_proof_narrative_contribution_renderer.py

変更する関数全体:
  suppress_toda_group_proof_narrative_repeated_unique_step_statements()

変更内容:
- 関数内だけに normalized_step_key() を追加
- canonical / public の双方で
    " は単射である" -> " は単射"
    " は全射である" -> " は全射"
  と正規化して比較
- connector_prefixes の "完全性より, " を維持

また repair6 の late dedup pass が存在することを確認し、
未適用時だけ追加する。

2. tests/test_phase159_exactness_map_property_public_dedup.py
- 最終 public renderer を直接検証
- pi_4^3 E 全射 1回
- pi_6^3 E 単射 1回

import 変更
===========
なし。

一般性
======
pi_4^3 / pi_6^3 / E 固有の判定は追加しない。
map property の文体差だけを unique-step dedup の比較キーで正規化する。

Phase 境界
==========
- exactness reason builder は変更しない。
- exactness reason renderer は変更しない。
- Reference statement match key の全体仕様は変更しない。
- equation numbering は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
