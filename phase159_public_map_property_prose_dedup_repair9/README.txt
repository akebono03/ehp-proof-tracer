Phase 159 - public map-property prose dedup repair9

原因
====
runtime audit により、重複は
_phase159_r1_7c_r4_normalize_public_map_property_prose()
で顕在化することが確定した。

Phase158 normalizer 出力には
  完全性より, E:... は単射.
と
  E:... は単射である.
が共存している。

Phase159 public prose normalizer が global replace で
  は単射である. -> は単射.
とするため、同じ map property が2回見える。

変更
====
- 従来の concise prose 正規化を維持
- "以上より, 完全性より, ..." を "完全性より, ..." に正規化
- exactness-qualified injective/surjective がある場合、
  同じ standalone map-property paragraph を抑制
- exactness reason がない standalone map property は維持

production import 変更
======================
なし。

repository-wide tests
=====================
Phase 159 終了時まで実行しない。
