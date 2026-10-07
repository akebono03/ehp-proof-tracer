Phase 159 pi3_2 numbered-map-property stale expectation repair9a

変更対象
========

test-only:
- tests/test_phase159_r1_2_pi3_2_narrative_repair.py
  - test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically()

production:
- 変更なし

import:
- 変更なし

理由
====

repair9 の新規 map-property order tests は 2/2 PASS。

残った既存 test failure は、旧 public contract:

  H ... は単射. (1)
  H ... は全射. (2)

という numbered display math を要求していた。

現在の public contract は:

  完全性より, H ... は単射.
  完全性より, H ... は全射.

という concise prose。

今回の Phase 159 方針でも
map-property の単射・全射はこの concise prose を採用している。

そのため production を番号付き表示へ戻さず、
test expectation を現在の contract へ更新する。

維持する semantic contract
==========================

必ず:

  H injective
  <
  H isomorphism

かつ:

  H surjective
  <
  H isomorphism

を要求する。

また旧 numbered display math が再び混入しないことも確認する。

境界
====

- repair9 production code は変更しない。
- repair8 pi4_3 fix は変更しない。
- repair7 pi6_3 fix は変更しない。
- equation numbering system 自体は変更しない。
- full suite は Phase 159 終了時まで実行しない。
