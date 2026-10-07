# Phase 159-R1-5

## 変更対象

Production:
- `toda_group_proof_narrative_renderer.py`
  - import
  - 新規 `_phase159_public_formula_map_property_line()`
  - 新規 `_phase159_normalize_public_map_property_wording()`
  - `render_toda_group_proof_narrative_markdown()`

Test:
- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`
  - 新規 `test_phase159_r1_5_pi3_2_public_map_property_wording_is_terse()`

## 変更後 import 部分

```python
from toda_group_proof_generic_narrative_renderer import (
  _GENERIC_INJECTIVE_STATEMENT_TYPES,
  _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  _GENERIC_ZERO_MAP_STATEMENT_TYPES,
  _generic_group_map_name,
  _render_generic_narrative_group_map_latex,
  _render_generic_narrative_step,
)
```

## 新規関数

`render_toda_group_proof_narrative_markdown()` の直前に追加する。

```python
def _phase159_public_formula_map_property_line(
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion

  if isinstance(
    statement,
    _GENERIC_INJECTIVE_STATEMENT_TYPES,
  ):
    property_label = "単射"
  elif isinstance(
    statement,
    _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  ):
    property_label = "全射"
  elif isinstance(
    statement,
    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  ):
    property_label = "同型"
  elif isinstance(
    statement,
    _GENERIC_ZERO_MAP_STATEMENT_TYPES,
  ):
    property_label = "零写像"
  else:
    return None

  group_map = getattr(
    statement,
    "map",
    None,
  )

  if group_map is None:
    return None

  map_latex = (
    _render_generic_narrative_group_map_latex(
      group_map
    )
  )

  if map_latex is None:
    return None

  return (
    "$"
    + map_latex
    + "$ は"
    + property_label
    + "."
  )


def _phase159_normalize_public_map_property_wording(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
  proof_index = rendered.find(
    proof_marker
  )

  if proof_index < 0:
    return rendered

  body_start = (
    proof_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :body_start
  ]
  proof_body = rendered[
    body_start:
  ]

  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  for node in semantic_presentation.nodes:
    proof_step = node.proof_step
    original = (
      _render_generic_narrative_step(
        proof_step
      )
    )
    replacement = (
      _phase159_public_formula_map_property_line(
        proof_step
      )
    )

    if replacement is None:
      continue

    proof_body = proof_body.replace(
      original,
      replacement,
    )

  return (
    prefix
    + proof_body
  )
```

## `render_toda_group_proof_narrative_markdown()` 全体

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )

  return (
    _phase159_normalize_public_map_property_wording(
      presentation,
      rendered,
    )
  )
```

## 追加テスト関数全体

```python
def test_phase159_r1_5_pi3_2_public_map_property_wording_is_terse():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は単射."
    in rendered
  )
  assert (
    r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
    "は零写像."
    in rendered
  )

  assert "は単射である." not in rendered
  assert "は全射である." not in rendered
  assert "は同型写像である." not in rendered
  assert "は零写像である." not in rendered
```

Test import 変更:
- なし

## 実行する pytest

Phase 159 focused:
```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
```

Related:
```powershell
python -m pytest -q `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
  ".\tests\test_phase143_42_argument_body_contribution_renderer.py" `
  ".\tests\test_phase49_generator_transport.py"
```

## 完了条件

- public proof body の map-property wording が
  `単射. / 全射. / 同型. / 零写像.` に統一される。
- Reference section は変更されない。
- Phase 159 focused tests PASS。
- related regressions PASS。
- `git diff --check` PASS。
- pi_3^2 実表示を確認する。

## 次 Phase との境界

R1-5 では Reference attribution を扱わない。
次は R1-6 で
- $\pi_2^1=0$
- $\pi_3^3=\mathbb Z\{\iota_3\}$
- $E:\pi_1^1\to\pi_2^2$ の同型
の出典を監査する。
