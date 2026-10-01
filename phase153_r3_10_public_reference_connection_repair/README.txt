Phase153-R3-10
Public Reference Connection Repair

目的
====
Phase153-R3-8 で public missing と分類された Reference statement を、
public Narrative の Reference section に接続する。

R3-8 classification
====================
- legacy_custom_reference_plus_proof: 14
- standard_reference_plus_proof: 3
- total: 17

変更対象
========
production:
- toda_group_proof_narrative_renderer.py

tests:
- tests/test_phase153_r3_10_public_reference_connection_repair.py

変更する関数
============
新規:
- _phase153_r3_10_connect_public_reference_section
  追加位置:
  _wrap_phase150_rc4_generic_public_narrative の直前

変更:
- _wrap_phase150_rc4_generic_public_narrative
- render_toda_group_proof_narrative_markdown

実装方針
========
1. legacy custom route
   既存の proof body はそのまま保持し、
   ## 使用する結果 から ## 証明 までだけを
   structured Reference pipeline の canonical section へ置き換える。

2. Phase150 generic public wrapper
   「最後の [Rn] title 行」で Reference section を切る旧方式を廃止する。
   structured Reference pipeline が生成した canonical reference_section を
   prefix として正確に切り分ける。

3. 既存 generic fallback route
   変更しない。

今回しないこと
==============
- renderer coverage
- representative selection
- Reference/body ownership
- duplicate suppression rule の拡張
- proof graph
- full pytest

完了条件
========
112 groups 全体について:
- selected statement の public Reference missing = 0
- structured Reference marker missing = 0
- R3-3〜R3-9 関連 targeted tests PASS

次 Phase との境界
================
R3-10 は public Reference connection まで。
R3-11 で exact body duplicates / ownership を扱う。
