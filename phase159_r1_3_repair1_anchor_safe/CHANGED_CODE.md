# Phase 159-R1-3 repair1

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - import
  - `_phase158_public_narrative_target_lines`
  - `_phase159_public_semantic_projection_context` 新規
  - `_phase159_matching_map_property_step` 新規
  - `_phase159_public_map_property_triples` 新規
  - `_phase159_numbered_map_property_line` 新規
  - `_phase159_plain_map_property_line` 新規
  - `_phase159_unique_preimage_definition_line` 新規
  - `_phase159_project_generic_semantics_to_public_proof` 新規
  - `_phase158_normalize_public_narrative_contract`
- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`
  - 全文更新

## import 変更後

```python
from toda_group_proof_generic_narrative_renderer import (
  _GENERIC_INJECTIVE_STATEMENT_TYPES,
  _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  _render_generic_narrative_group_map_latex,
  _render_generic_narrative_step,
)
```

```python
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_method_renderer import (
  render_toda_group_proof_narrative_exactness_method_component_latex,
)
```

`from toda_group_proof_narrative_semantics import (...)` には
`TodaGroupProofNarrativeDependencySemanticRole` を追加する。

変更関数・新規関数・テストの完全なコードは
`apply_phase159_r1_3_repair1.py` 内に省略なしで収録している。

## focused pytest

- tests/test_phase159_r1_2_pi3_2_narrative_repair.py
- tests/test_phase159_r1_2_hopf_injective_dependency_role.py
- tests/test_phase159_r1_2_hopf_isomorphism_dependency_role.py
- tests/test_phase143_32_exactness_component_latex.py
- tests/test_phase143_42_argument_body_contribution_renderer.py
- tests/test_phase143_2_generic_short_exact_sequence.py
- tests/test_phase150_rc4_5c_2_exactness_to_map_property.py

## 完了条件

- 証明対象から `を示す.` が消える。
- 証明対象の period は display math 内。
- overlapping exactness windows は connected component 1本。
- injective / surjective は numbered intermediate facts。
- `(1) と (2) より` isomorphism。
- PRECONDITION_FOR_DEFINITION + isomorphism から unique preimage prose。
- terminal QED 維持。
- focused tests / regressions / `git diff --check` PASS。

## 次 Phase との境界

変更しない:
- Reference attribution
- stable-range 判定
- Freudenthal 自動処理
- 新 theorem / lemma
- 全体 prose refactor
