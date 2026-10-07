Phase 159 - exactness map-property public dedup repair8

原因
====
pi_6^3 では同じ表示を持つ injective map-property proof step が複数存在し得るため、
既存 unique-step dedup の

  len(step_ids) == 1

という条件では E の単射性が dedup 対象にならない。

一方、今回の public prose では exactness reason がすでに

  完全性より, E:... は単射.

という理由付き結論を持つ。

この場合、同じ map property の standalone

  E:... は単射.

を残す必要はない。

変更対象
========
toda_group_proof_narrative_contribution_renderer.py

変更する関数全体:
  suppress_toda_group_proof_narrative_repeated_unique_step_statements()

処理
====
1. "完全性より, " で始まる paragraph を先に収集する。
2. その本文が "は単射" または "は全射" で終わる map property のとき、
   normalized key を exactness_map_property_keys に記録する。
3. 同じ key の standalone paragraph は、proof-step 数に関係なく抑制する。
4. exactness-qualified paragraph は最初の1つだけ残す。
5. その他の statement には従来の unique-step dedup をそのまま使う。

一般性
======
pi_4^3 / pi_6^3 / E / H / Delta 固有判定は追加しない。
exactness-qualified injective/surjective map property 全般に適用する。

テスト
======
tests/test_phase159_exactness_map_property_public_dedup.py

最終 public renderer で:
- pi_4^3 E 全射が1回
- pi_6^3 E 単射が1回

を確認する。

Phase 境界
==========
- exactness reason builder は変更しない。
- exactness reason renderer は変更しない。
- Reference selection は変更しない。
- equation numbering は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
