# Phase 159-R1-6d

## 変更対象

### production
- `toda_group_proof_narrative_renderer.py`
  - 新規 `_phase159_r1_6d_toda_51_diagonal_specialization_lines()`
  - 新規 `_phase159_r1_6d_finalize_reference_and_linkage()`
  - 新規 `_phase159_r1_6d_center_structural_formulas()`
  - `render_toda_group_proof_narrative_markdown()`

import:
- 変更なし

class:
- 変更なし

### tests
- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`
  - `test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence()`
  - `test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically()`
- `tests/test_phase159_r1_6b_toda51_attribution.py`
  - `test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement()`
- `tests/test_phase159_r1_6c_source_faithful_reference_linkage.py`
  - 4 test functions
- 新規 `tests/test_phase159_r1_6d_specialization_reference_linkage_finalization.py`

## 表示契約

Reference:

```text
[R1] (5.1).
pi_i^1 = 0 (i>1), pi_i^n = 0 (i<n).
pi_n^n = Z{iota_n}.
```

Proof:

```text
[R1] より, pi_1^1 = Z{iota_1}, pi_2^2 = Z{iota_2}.

E(iota_1)=iota_2 であるから,
E:pi_1^1 -> pi_2^2 は同型.
```

完全列と番号付き重要式は display math として中央揃えにする。

## 完了条件

- `pi_n^n` が `Z{iota_n}` 表記。
- `[R1] より` に空白統一。
- E 同型の特殊化根拠が本文に出る。
- 完全列が中央揃え。
- (1), (2) の重要式が中央揃え。
- R1-6d focused PASS。
- R1-6a/b/c PASS。
- Phase159 focused PASS。
- related regressions PASS。
- `git diff --check` PASS。
- full pytest は未実行。

## 次 Phase との境界

R1-6d は public Narrative の `(5.1)` specialization / linkage の最終化のみ。
proof DAG の低次元 E 同型を別 inference chain に作り直すことや、他文献 locator の表示再設計は行わない。
