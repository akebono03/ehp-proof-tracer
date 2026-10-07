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

  if stem not in (
    1,
    2,
    7,
  ):
    return None

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

  target_generator = (
    group_structure.generator
  )

  if stem == 1:
    target_generator_symbol = getattr(
      target_generator,
      "generator",
      None,
    )

    if (
      order != 2
      or target_generator_symbol is None
      or getattr(
        target_generator_symbol,
        "family",
        None,
      )
      != "η"
      or getattr(
        target_generator_symbol,
        "index",
        None,
      )
      != sphere_dimension
    ):
      return None

    reference_locator = (
      "Proposition 5.1"
    )
    base_generator_latex = (
      r"\eta_{3}"
    )
    target_generator_latex = (
      r"\eta_{"
      + str(
        sphere_dimension
      )
      + "}"
    )

  elif stem == 2:
    if (
      order != 2
      or type(
        target_generator
      ).__name__
      != "Composition"
    ):
      return None

    left = getattr(
      target_generator,
      "left",
      None,
    )
    right = getattr(
      target_generator,
      "right",
      None,
    )
    left_symbol = getattr(
      left,
      "generator",
      None,
    )
    right_symbol = getattr(
      right,
      "generator",
      None,
    )

    if (
      left_symbol is None
      or right_symbol is None
      or getattr(
        left_symbol,
        "family",
        None,
      )
      != "η"
      or getattr(
        right_symbol,
        "family",
        None,
      )
      != "η"
      or getattr(
        left_symbol,
        "index",
        None,
      )
      != sphere_dimension
      or getattr(
        right_symbol,
        "index",
        None,
      )
      != sphere_dimension + 1
    ):
      return None

    reference_locator = (
      "Proposition 5.3"
    )
    base_generator_latex = (
      r"\eta_{4}^{2}"
    )
    target_generator_latex = (
      r"\eta_{"
      + str(
        sphere_dimension
      )
      + r"}^{2}"
    )

  else:
    target_generator_symbol = getattr(
      target_generator,
      "generator",
      None,
    )

    if (
      order != 16
      or target_generator_symbol is None
      or getattr(
        target_generator_symbol,
        "family",
        None,
      )
      != "σ"
      or getattr(
        target_generator_symbol,
        "index",
        None,
      )
      != sphere_dimension
    ):
      return None

    reference_locator = (
      "Proposition 5.15"
    )
    base_generator_latex = (
      r"\sigma_{9}"
    )
    target_generator_latex = (
      r"\sigma_{"
      + str(
        sphere_dimension
      )
      + "}"
    )

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
