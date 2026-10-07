# Phase 159 `pi_(n+1)^n` stable transport repair1

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - 新規: `_phase159_render_pi_n_plus_1_n_stable_transport_narrative`
  - 変更: `render_toda_group_proof_narrative_markdown`
- `tests/test_phase159_pi_nplus1_n_stable_transport.py`
  - 新規 focused tests

import の変更はありません。

## 追加位置

`_phase159_render_pi_n_plus_1_n_stable_transport_narrative` は、
`render_toda_group_proof_narrative_markdown` の直前に追加します。

## 新規関数全文

```python
def _phase159_render_pi_n_plus_1_n_stable_transport_narrative(
  presentation: TodaGroupProofPresentation,
) -> str | None:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )
  sphere_dimension = target.sphere_dimension
  group_dimension = target.group_dimension

  if (
    isinstance(
      sphere_dimension,
      bool,
    )
    or not isinstance(
      sphere_dimension,
      int,
    )
    or isinstance(
      group_dimension,
      bool,
    )
    or not isinstance(
      group_dimension,
      int,
    )
  ):
    return None

  if (
    sphere_dimension < 4
    or group_dimension
    != sphere_dimension + 1
  ):
    return None

  suspension_exponent = (
    sphere_dimension - 3
  )

  lines = [
    "# Group proof narrative",
    "",
    "## 証明対象",
    "",
    r"\[",
    (
      rf"\pi_{{{group_dimension}}}^{{{sphere_dimension}}} "
      rf"= \mathbb{{Z}}/2\{{\eta_{{{sphere_dimension}}}\}}."
    ),
    r"\]",
    "",
    "## 使用する結果",
    "",
    "**[R1] (4.5).**",
    r"$n \ge k + 2$ のとき,",
    (
      r"$E^{m - n}: \pi_{n + k}^{n} "
      r"\to \pi_{m + k}^{m}$ は同型."
    ),
    "**[R2] Proposition 5.1.**",
    r"$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.",
    "",
    "---",
    "",
    "## 証明",
    "",
    (
      rf"$\pi_{{{group_dimension}}}^{{{sphere_dimension}}}$ "
      "の群構造を決定する."
    ),
    "",
    (
      r"[R2]より, "
      r"$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$."
    ),
    "",
    (
      r"[R1]を "
      rf"$(n,m,k)=(3,{sphere_dimension},1)$ "
      r"に適用する. "
      r"$3 \ge 1 + 2$ なので適用条件を満たし,"
    ),
    "",
    r"\[",
    (
      rf"E^{{{suspension_exponent}}}: "
      rf"\pi_{{4}}^{{3}} \longrightarrow "
      rf"\pi_{{{group_dimension}}}^{{{sphere_dimension}}}"
    ),
    r"\]",
    "",
    "は同型.",
    "",
    r"$\eta$-family の定義より,",
    "",
    r"\[",
    (
      rf"E^{{{suspension_exponent}}}\eta_{{3}} "
      rf"= \eta_{{{sphere_dimension}}}."
    ),
    r"\]",
    "",
    "したがって,",
    "",
    r"\[",
    (
      rf"\pi_{{{group_dimension}}}^{{{sphere_dimension}}} "
      rf"= \mathbb{{Z}}/2\{{\eta_{{{sphere_dimension}}}\}}."
    ),
    r"\]",
    "",
    "□",
    "",
  ]

  return "\n".join(
    lines
  )
```

## 変更関数全文

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  stable_transport_rendered = (
    _phase159_render_pi_n_plus_1_n_stable_transport_narrative(
      presentation
    )
  )

  if stable_transport_rendered is not None:
    return stable_transport_rendered

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
  rendered = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  return (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )
```

## 新規テスト全文

```python
import pytest

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


@pytest.mark.parametrize(
  "n",
  (
    4,
    5,
    6,
  ),
)
def test_phase159_pi_nplus1_n_uses_common_toda45_transport_proof(
  n,
):
  presentation, _, _, _ = (
    _method_evidence_data(
      n,
      1,
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  exponent = n - 3

  assert "**[R1] (4.5).**" in rendered
  assert (
    "$n \\ge k + 2$ のとき,"
    in rendered
  )
  assert (
    "$E^{m - n}: \\pi_{n + k}^{n} "
    "\\to \\pi_{m + k}^{m}$ は同型."
    in rendered
  )
  assert (
    "**[R2] Proposition 5.1.**"
    in rendered
  )
  assert (
    "$\\pi_{4}^{3} = "
    "\\mathbb{Z}/2\\{\\eta_{3}\\}$."
    in rendered
  )
  assert (
    f"$(n,m,k)=(3,{n},1)$"
    in rendered
  )
  assert (
    f"E^{{{exponent}}}: "
    f"\\pi_{{4}}^{{3}} \\longrightarrow "
    f"\\pi_{{{n + 1}}}^{{{n}}}"
    in rendered
  )
  assert (
    f"E^{{{exponent}}}\\eta_{{3}} "
    f"= \\eta_{{{n}}}."
    in rendered
  )
  final_result = (
    f"\\pi_{{{n + 1}}}^{{{n}}} "
    f"= \\mathbb{{Z}}/2\\{{\\eta_{{{n}}}\\}}."
  )
  assert rendered.count(
    final_result
  ) == 2
  assert "\\tag{" not in rendered


def test_phase159_pi5_4_does_not_rederive_generic_target_family_in_body():
  presentation, _, _, _ = (
    _method_evidence_data(
      4,
      1,
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{E^{n - 3}\eta_{3}\}"
    not in proof_body
  )
  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    not in proof_body
  )
  assert (
    r"E^{n - 3}: \pi_{3 + 1}^{3} "
    r"\to \pi_{n + 1}^{n}"
    not in rendered
  )


def test_phase159_pi4_3_remains_on_existing_narrative_route():
  presentation, _, _, _ = (
    _method_evidence_data(
      3,
      1,
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}."
    in rendered
  )
  assert (
    r"\operatorname{Im}\Delta"
    in rendered
  )
  assert "**[R1] (4.5).**" not in rendered
```
