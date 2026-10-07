# Phase 159-R1-3 changed code

変更対象:
- `toda_group_proof_narrative_renderer.py`
- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`

Production の import 変更、新規 helper、変更関数、Test 全文は
`apply_phase159_r1_3.py` に省略なしで収録している。

実装の中心:
1. `_phase158_public_narrative_target_lines`
   - 「を示す.」を削除。
   - display math の数式末尾に `.` を置く。

2. `_phase159_public_exactness_component`
   - semantic closure -> blocks -> exactness components の既存経路を再利用。
   - target を含む一意な component のみ public projection 対象とする。

3. `_phase159_public_map_property_triples`
   - 同一 map に対する injective / surjective / isomorphism を semantic statement type から対応付ける。

4. `_phase159_project_generic_semantics_to_public_proof`
   - constituent exactness windows を1本の component 表示へ縮約。
   - injective / surjective を numbered facts として表示。
   - isomorphism を `(1) と (2) より` で接続。
   - isomorphism map と一致する map/element/image definition を unique preimage prose にする。

5. `_phase158_normalize_public_narrative_contract`
   - 既存 equation normalization の直後で Phase 159 semantic projection を呼ぶ。

テスト:
- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py` を全文置換。
- exactness component の既存 regression tests は変更せず実行する。
