Phase 159 pi3_2 map-property order repair9

変更対象
========

production:
- toda_group_proof_narrative_reason_renderer.py
  - order_toda_group_proof_narrative_injective_image_order_reason()

new test:
- tests/test_phase159_pi3_2_map_property_order.py

import:
- 変更なし

監査結果
========

pi3_2 の BASE では

  H: pi3^2 -> pi3^3 は同型写像である.

が既に visible。

その後 reason / contribution pipeline で

  H は全射
  H は単射

が追加されるため、最終 public output が

  H 同型
  H 全射
  H 単射

となっていた。

現行 Phase 159 既存 test も

  injective < isomorphism
  surjective < isomorphism

を要求しており、実際に regression failure を確認した。

修正規則
========

同じ semantic map object を持つ map-property statements について、

- visible injective reason がある
- visible surjective reason がある
- visible proof-internal isomorphism statement がある

場合だけ、

  injective / surjective
  <
  isomorphism

となるよう isomorphism paragraph を後ろへ移動する。

reference prefix や reason wording の単純文字列だけではなく、
statement.map の equality を使って同じ写像を識別する。

E isomorphism について
======================

E: pi1^1 -> pi2^2 の fixed literature statement は、
同じ map について injective と surjective の両 reason が揃わないため
この移動対象にならない。

したがって

  [R1]より E は同型
  -> E は単射
  -> Delta=0

という前提側の流れは維持できる。

期待する pi3_2 order
====================

1. pi2^1 = 0
2. H injective
3. [R1] E isomorphism
4. E injective
5. Delta zero
6. pi3^3 = Z{iota3}
7. H surjective
8. H isomorphism
9. eta2 unique Hopf preimage
10. pi3^2 = Z{eta2}

今回の repair9 はまず
H injective / H surjective < H isomorphism
の一般 contract を修復する。

境界
====

- repair8 provider-anchor upper bound は変更しない。
- pi4_3 trailing-premise fix は変更しない。
- pi6_3 repair7 は変更しない。
- contribution placement classification は変更しない。
- full suite は Phase 159 終了時まで実行しない。
