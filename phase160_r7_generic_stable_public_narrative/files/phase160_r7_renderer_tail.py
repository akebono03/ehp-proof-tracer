# Phase160-R7 generic stable finite-cyclic public narrative
_phase160_r7_previous_public_narrative_renderer = (
  _phase159_repair3_previous_public_narrative_renderer
)


def _phase160_r7_render_stable_finite_cyclic_transport_narrative(
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

  group_result = (
    presentation
    .source_replay
    .group_result
  )
  target = group_result.target
  sphere_dimension = target.sphere_dimension
  group_dimension = target.group_dimension
  group_structure = group_result.group_structure

  if (
    not isinstance(
      sphere_dimension,
      int,
    )
    or isinstance(
      sphere_dimension,
      bool,
    )
    or not isinstance(
      group_dimension,
      int,
    )
    or isinstance(
      group_dimension,
      bool,
    )
  ):
    return None

  stem = (
    group_dimension
    - sphere_dimension
  )

  stable_family_contract = {
    1: (
      "Proposition 5.1",
      "η",
      r"\eta",
    ),
    7: (
      "Proposition 5.15",
      "σ",
      r"\sigma",
    ),
  }

  contract = (
    stable_family_contract.get(
      stem
    )
  )

  if contract is None:
    return None

  (
    reference_locator,
    expected_family,
    family_latex,
  ) = contract

  base_sphere_dimension = (
    stem + 2
  )

  if (
    sphere_dimension
    <= base_sphere_dimension
  ):
    return None

  if (
    type(
      group_structure
    ).__name__
    != "FiniteCyclicGroup"
  ):
    return None

  target_generator = (
    group_structure.generator
  )
  target_generator_symbol = getattr(
    target_generator,
    "generator",
    None,
  )

  if (
    target_generator_symbol is None
    or getattr(
      target_generator_symbol,
      "family",
      None,
    )
    != expected_family
    or getattr(
      target_generator_symbol,
      "index",
      None,
    )
    != sphere_dimension
  ):
    return None

  order = group_structure.order

  if (
    not isinstance(
      order,
      int,
    )
    or isinstance(
      order,
      bool,
    )
    or order <= 0
  ):
    return None

  base_group_dimension = (
    base_sphere_dimension
    + stem
  )
  suspension_exponent = (
    sphere_dimension
    - base_sphere_dimension
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

  base_group_latex = (
    r"\pi_{"
    + str(
      base_group_dimension
    )
    + r"}^{"
    + str(
      base_sphere_dimension
    )
    + "}"
  )

  target_group_latex = (
    render_toda_primary_group_latex(
      target
    )
  )

  base_generator_latex = (
    family_latex
    + "_{"
    + str(
      base_sphere_dimension
    )
    + "}"
  )

  target_generator_latex = (
    render_toda_expression_latex(
      target_generator
    )
  )

  group_prefix_latex = (
    r"\mathbb{Z}/"
    + str(
      order
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
        target_group_latex
        + " = "
        + group_prefix_latex
        + r"\{"
        + target_generator_latex
        + r"\}."
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
      (
        "**[R2] "
        + reference_locator
        + ".**"
      ),
      (
        r"$"
        + base_group_latex
        + " = "
        + group_prefix_latex
        + r"\{"
        + base_generator_latex
        + r"\}$."
      ),
      "",
      "---",
      "",
      "## 証明",
      "",
      (
        r"$"
        + target_group_latex
        + r"$ の群構造を決定する."
      ),
      "",
      (
        r"[R2]より, "
        r"$"
        + base_group_latex
        + " = "
        + group_prefix_latex
        + r"\{"
        + base_generator_latex
        + r"\}$."
      ),
      "",
      (
        r"[R1]を "
        r"$(n,m,k)=("
        + str(
          base_sphere_dimension
        )
        + ","
        + str(
          sphere_dimension
        )
        + ","
        + str(
          stem
        )
        + r")$ に適用すると, "
        r"$"
        + suspension_latex
        + ": "
        + base_group_latex
        + r" \to "
        + target_group_latex
        + r"$ は同型."
      ),
      "",
      (
        r"$"
        + suspension_latex
        + base_generator_latex
        + " = "
        + target_generator_latex
        + r"$."
      ),
      "",
      (
        r"以上より, "
        r"$"
        + target_group_latex
        + " = "
        + group_prefix_latex
        + r"\{"
        + target_generator_latex
        + r"\}$."
      ),
      "",
      "□",
      "",
    )
  )


def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  stable_transport_narrative = (
    _phase160_r7_render_stable_finite_cyclic_transport_narrative(
      presentation
    )
  )

  if stable_transport_narrative is not None:
    return stable_transport_narrative

  return (
    _phase160_r7_previous_public_narrative_renderer(
      presentation
    )
  )
