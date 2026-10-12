# Phase 163 R4-R66 登録単位の暫定判定

**採用方針:** 文献上の Reference は原則1項目、複数の独立した定義があれば Assertion を個別に番号付けする。
この判定は編集上の区分のみ。原本照合・数学的検証・正式登録・ID採番・証明探索への接続はしていない。

|章|候補|Reference|Assertion|区分|要確認事項|
|---:|---|---:|---:|---|---|
|1|`unit_sphere`|1|1|SINGLE_ASSERTION|なし（原本照合は別途必要）|
|1|`pointed_homotopy_classes`|1|1|SINGLE_ASSERTION|TRAILING_SENTENCE_OUTSIDE_SPAN|
|1|`composition_homotopy_classes`|1|1|SINGLE_ASSERTION|CONTEXT_FOR_COMPOSITION|
|1|`iterated_suspension`|1|1|SINGLE_ASSERTION|なし（原本照合は別途必要）|
|1|`addition_inverse_suspension`|1|2|TWO_DEFINITIONS_IN_ONE_BLOCK|なし（原本照合は別途必要）|
|1|`secondary_composition`|1|1|SINGLE_ASSERTION|PRECEDING_CONSTRUCTION_REQUIRED|
|1|`reduced_cone`|1|1|SINGLE_ASSERTION|なし（原本照合は別途必要）|
|1|`extension`|1|1|SINGLE_ASSERTION|ATTACHING_SPACE_CONTEXT_REQUIRED|
|1|`coextension`|1|1|SINGLE_ASSERTION|ATTACHING_SPACE_CONTEXT_REQUIRED|
|3|`stable_homotopy_group`|1|2|GROUP_AND_MAP_IN_ONE_BLOCK|SOURCE_ENDS_AT_DISPLAY|
|3|`stable_composition`|1|1|SINGLE_ASSERTION|なし（原本照合は別途必要）|
|3|`stable_toda_bracket`|1|1|SINGLE_ASSERTION|DEFINITION_HYPOTHESES_AND_INDETERMINACY|
|5|`nu4_generator_notation`|1|1|SINGLE_ASSERTION|PRIOR_CHOICES_ALPHA_STAR_U_S|
|5|`nu_n_notation`|1|2|UNSTABLE_AND_STABLE_SYMBOLS|ADJACENT_NOTATION_BLOCK|
|5|`eta_n_cubed_notation`|1|2|UNSTABLE_AND_STABLE_SYMBOLS|ADJACENT_NOTATION_BLOCK|
|5|`nu_n_squared_notation`|1|2|UNSTABLE_AND_STABLE_SYMBOLS|なし（原本照合は別途必要）|

## R4-R67 の対象

出典範囲の切れ目と前提条件の不足を優先して見直す。必要なら Reference の出典範囲のみ拡張する。
数学的な検証結果なしに `mathematical_boundary_verified` を真にしない。

## 限定テスト

`python -m pytest -q phase163_r4_r66_multi_assertion_boundary/tests/test_phase163_r4_r66_multi_assertion_boundary.py`

全体 pytest は Phase 163 の最後に実施する。
