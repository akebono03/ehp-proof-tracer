Phase 159 pi6_3 zero-map reason-order repair7

変更対象
========

production:
- toda_group_proof_narrative_contribution_renderer.py
  - insert_toda_group_proof_narrative_hidden_zero_map_premises()

new test:
- tests/test_phase159_pi6_3_zero_map_reason_order.py

import:
- 変更なし

根本原因
========

reason insertion が先に

  完全性より, $E: pi5^2 -> pi6^3$ は単射.

を consumer の直前へ置く。

その後 hidden-zero-map insertion が

  Delta: pi7^5 -> pi5^2 は零写像.

を consumer の直前へ置く。

既存コードは consumer 直前の paragraph が

- 零写像
- Delta=0
- ker E = Im Delta ...

の場合だけ insertion point を1つ前へ戻していた。

Phase 159 の concise reason はこの条件に入らないため、

  concise reason
  zero-map
  consumer

という逆順になった。

修正
====

consumer step の generic rendered statement から、

  は単射である. -> は単射.
  は全射である. -> は全射.

へ正規化した concise map-property reason

  完全性より, <concise conclusion>

を算出する。

consumer 直前 paragraph がこの reason と一致する場合も、
zero-map insertion point を1つ前へ戻す。

結果:

  zero-map
  concise reason
  consumer

となる。

pi6_3 固有の n/k 分岐や式文字列は使用しない。

テスト
======

新規:
- contribution renderer:
  zero-map < concise injectivity reason
- public renderer:
  zero-map < concise injectivity reason

既存 regression:
- Phase 150 exactness reason
- Phase 157 dangling connector
- Phase 157 zero-map/use order
- Phase 159 pi4_3 repair5 focused tests

境界
====

- pi4_3 repair5 は変更しない。
- reason renderer は変更しない。
- public contract normalization は変更しない。
- heavy Phase 144 cross-group fixture は実行しない。
- full test suite は Phase 159 終了時まで実行しない。
