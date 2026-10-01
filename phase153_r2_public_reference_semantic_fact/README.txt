Phase 153-R2 Public Narrative Repair
====================================

目的
----
R2 で Toda45IsomorphismStatement を MAP_PROPERTY として分類し、
generic renderer で同型写像として表示可能にしたが、
legacy/reference public Narrative では reference marker が semantic fact を
置き換えていた。

今回の変更
----------
1. toda_group_proof_narrative_renderer.py
   - generic step renderer を利用する。
   - provenance-only predicate を利用する。
   - reference-bearing leaf premise について次の一般規則を適用する。

     provenance-only:
       reference marker のみ。

     non-provenance-only かつ meaningful generic rendering:
       reference marker + semantic fact。

     non-provenance-only だが generic fallback:
       reference marker のみ。

2. tests/test_phase153_r2_public_reference_semantic_fact.py
   - pi_10^6 depth 2 public Narrative で [R2] と Toda 4.5 の同型写像内容が
     同時に表示されることを確認する。
   - provenance-only の [R1] Proposition 5.8 は従来どおり compact reference
     のままであることを確認する。

境界
----
- Toda45IsomorphismStatement 専用分岐は追加しない。
- TodaProp42ExactnessStatement の既存互換処理は今回は変更しない。
- unresolved rendering 2件の renderer は今回追加しない。
- generic public route の対象拡大はしない。
- theorem logic / group result / API は変更しない。
- repository-wide pytest は Phase 153 終了時まで実行しない。
