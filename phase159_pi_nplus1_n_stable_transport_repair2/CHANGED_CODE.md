# Phase 159 pi_(n+1)^n stable transport repair2

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - 新規関数 `_phase159_render_pi_n_plus_1_n_stable_transport_narrative`
  - 変更関数 `render_toda_group_proof_narrative_markdown`
- `tests/test_phase159_pi_nplus1_n_stable_transport.py`
  - 新規 focused tests

import の変更はありません。

## 追加位置

`_phase159_render_pi_n_plus_1_n_stable_transport_narrative` は
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
  sphere_dimension = (
    target.sphere_dimension
  )
  group_dimension = (
    target.group_dimension
  )

  if (
    not isinstance(
      sphere_dimension,
      int,
    )
    or not isinstance(
      group_dimension,
      int,
    )
    or sphere_dimension < 4
    or group_dimension
    != sphere_dimension + 1
  ):
    return None

  target_n = sphere_dimension
  suspension_exponent = (
    target_n - 3
  )
  suspension_latex = (
    "E"
    if suspension_exponent == 1
    else (
      "E^{"
      + str(
        suspension_exponent
      )
      + "}"
    )
  )

  return "\n".join(
    (
      "# Group proof narrative",
      "",
      "## 証明対象",
      "",
      r"\[",
      (
        r"\pi_{"
        + str(
          target_n + 1
        )
        + r"}^{"
        + str(
          target_n
        )
        + r"} = "
        + r"\mathbb{Z}/2\{\eta_{"
        + str(
          target_n
        )
        + r"}\}."
      ),
      r"\]",
      "",
      "## 使用する結果",
      "",
      "**[R1] (4.5).**",
      (
        r"$n \ge k + 2$ のとき, "
        r"$E^{m-n}: "
        r"\pi_{n+k}^{n} "
        r"\to "
        r"\pi_{m+k}^{m}$ は同型."
      ),
      "",
      "**[R2] Proposition 5.1.**",
      (
        r"$\pi_{4}^{3} = "
        r"\mathbb{Z}/2\{\eta_{3}\}$."
      ),
      "",
      "---",
      "",
      "## 証明",
      "",
      (
        r"$\pi_{"
        + str(
          target_n + 1
        )
        + r"}^{"
        + str(
          target_n
        )
        + r"}$ の群構造を決定する."
      ),
      "",
      (
        r"[R2]より, "
        r"$\pi_{4}^{3} = "
        r"\mathbb{Z}/2\{\eta_{3}\}$."
      ),
      "",
      (
        r"[R1]を "
        r"$(n,m,k)=(3,"
        + str(
          target_n
        )
        + r",1)$ に適用すると, "
        r"$"
        + suspension_latex
        + r": \pi_{4}^{3} "
        r"\to "
        r"\pi_{"
        + str(
          target_n + 1
        )
        + r"}^{"
        + str(
          target_n
        )
        + r"}$ は同型."
      ),
      "",
      (
        r"$"
        + suspension_latex
        + r"\eta_{3} = "
        r"\eta_{"
        + str(
          target_n
        )
        + r"}$."
      ),
      "",
      (
        r"以上より, "
        r"$\pi_{"
        + str(
          target_n + 1
        )
        + r"}^{"
        + str(
          target_n
        )
        + r"} = "
        r"\mathbb{Z}/2\{\eta_{"
        + str(
          target_n
        )
        + r"}\}$."
      ),
      "",
      "□",
      "",
    )
  )

```

## 変更後の関数全文

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  stable_transport_narrative = (
    _phase159_render_pi_n_plus_1_n_stable_transport_narrative(
      presentation
    )
  )

  if stable_transport_narrative is not None:
    return stable_transport_narrative

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
  rendered = (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )

  return (
    _phase159_r1_6d_finalize_reference_and_linkage(
      presentation,
      _phase159_order_public_unique_preimage_definition_premises(
        presentation,
        rendered,
      ),
    )
  )

```

## 新規テストファイル全文

```python
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _render(
  n: int,
) -> str:
  presentation, _, _, _ = (
    _method_evidence_data(
      n,
      1,
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def test_phase159_pi5_4_uses_prop51_and_general_toda45_reference():
  rendered = _render(
    4
  )

  assert (
    "**[R1] (4.5).**"
    in rendered
  )
  assert (
    r"$n \ge k + 2$ のとき, "
    r"$E^{m-n}: "
    r"\pi_{n+k}^{n} "
    r"\to "
    r"\pi_{m+k}^{m}$ は同型."
    in rendered
  )
  assert (
    "**[R2] Proposition 5.1.**"
    in rendered
  )
  assert (
    r"$\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}$."
    in rendered
  )


def test_phase159_pi5_4_specializes_toda45_in_proof_body():
  rendered = _render(
    4
  )
  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  assert (
    r"[R1]を $(n,m,k)=(3,4,1) "
    r"に適用すると, "
    r"$E: \pi_{4}^{3} "
    r"\to \pi_{5}^{4}$ は同型."
    in proof_body
  )
  assert (
    r"$E\eta_{3} = \eta_{4}$."
    in proof_body
  )
  assert (
    r"$\pi_{n + 1}^{n}"
    not in proof_body
  )
  assert (
    r"\tag{"
    not in proof_body
  )


def test_phase159_pi_nplus1_n_family_uses_same_stable_transport_proof():
  cases = (
    (
      5,
      r"$E^{2}: \pi_{4}^{3} "
      r"\to \pi_{6}^{5}$ は同型.",
      r"$E^{2}\eta_{3} = \eta_{5}$.",
      r"$\pi_{6}^{5} = "
      r"\mathbb{Z}/2\{\eta_{5}\}$.",
    ),
    (
      6,
      r"$E^{3}: \pi_{4}^{3} "
      r"\to \pi_{7}^{6}$ は同型.",
      r"$E^{3}\eta_{3} = \eta_{6}$.",
      r"$\pi_{7}^{6} = "
      r"\mathbb{Z}/2\{\eta_{6}\}$.",
    ),
  )

  for (
    n,
    isomorphism,
    generator_transport,
    conclusion,
  ) in cases:
    rendered = _render(
      n
    )

    assert (
      "**[R1] (4.5).**"
      in rendered
    )
    assert (
      "**[R2] Proposition 5.1.**"
      in rendered
    )
    assert (
      isomorphism
      in rendered
    )
    assert (
      generator_transport
      in rendered
    )
    assert (
      conclusion
      in rendered
    )


def test_phase159_pi4_3_does_not_use_stable_transport_family_renderer():
  rendered = _render(
    3
  )

  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
    in rendered
  )
  assert (
    r"$(n,m,k)=(3,3,1)"
    not in rendered
  )
  assert (
    r"\operatorname{Im}\Delta"
    in rendered
  )

```

## 今回の境界

- 対象は `pi_(n+1)^n`, `n >= 4` のみ。
- `pi_4^3` の exactness 証明は変更しない。
- Toda (4.5) の inference rule 自体は変更しない。
- Proposition 5.1 の既存 proof graph は変更しない。
- 全体テストは Phase の最後まで実行しない。
