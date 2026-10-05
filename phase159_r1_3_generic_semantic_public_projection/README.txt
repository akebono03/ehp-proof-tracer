Phase 159-R1-3
================

目的
----
既に存在する generic semantic structure を public presentation まで正しく通す。

今回の最小変更
--------------
Production:
- toda_group_proof_narrative_renderer.py
  - generic map-property type tuple / map renderer の import を追加
  - exactness component builder / renderer の import を追加
  - _phase158_public_narrative_target_lines()
  - _phase159_public_exactness_component() 新規
  - _phase159_public_map_property_triples() 新規
  - _phase159_numbered_map_property_line() 新規
  - _phase159_plain_map_property_line() 新規
  - _phase159_unique_preimage_definition_line() 新規
  - _phase159_project_generic_semantics_to_public_proof() 新規
  - _phase158_normalize_public_narrative_contract() から上記 projection を呼ぶ

Test:
- tests/test_phase159_r1_2_pi3_2_narrative_repair.py
  - public contract を Phase 159-R1-3 仕様へ更新

実装原則
--------
- pi_3^2 の target dimension による専用分岐は追加しない。
- exactness は既存 component builder が作る ordered component を public 表示へ投影する。
- injective / surjective / isomorphism は同一 map の semantic relation から接続する。
- unique preimage prose は map / element / image と isomorphism の対応から生成する。
- raw proof provenance は変更しない。
- theorem/rule の数学的内容は変更しない。
- Reference attribution は変更しない。
- full test suite は実行しない。

完了条件
--------
1. 証明対象から「を示す.」が消える。
2. 証明対象の display math の末尾に period が入る。
3. pi_3^2 の overlapping exactness windows が public 本文では1本の exactness component に統合される。
4. H の単射・全射が番号付きで表示される。
5. その番号から H の同型が導かれる。
6. eta_2 は H の同型性から unique preimage として自然に導入される。
7. QED は維持される。
8. focused regression が PASS する。

次 Phase との境界
-----------------
今回行わないこと:
- 新しい数学定理・lemma の追加
- stable range 判定
- Freudenthal 自動終了
- Reference attribution の再設計
- 他の prose 全般のリファクタリング
