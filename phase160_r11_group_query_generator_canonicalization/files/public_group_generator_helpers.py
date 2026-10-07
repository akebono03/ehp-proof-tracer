def _toda_public_eta_composition_factors(
  expression,
) -> tuple[
  HomotopyElement,
  ...,
] | None:
  if isinstance(
    expression,
    Composition,
  ):
    left = (
      _toda_public_eta_composition_factors(
        expression.left
      )
    )
    right = (
      _toda_public_eta_composition_factors(
        expression.right
      )
    )

    if (
      left is None
      or right is None
    ):
      return None

    return (
      left
      + right
    )

  if not isinstance(
    expression,
    HomotopyElement,
  ):
    return None

  generator = expression.generator

  if (
    generator is None
    or generator.family != "η"
    or not isinstance(
      generator.index,
      int,
    )
    or isinstance(
      generator.index,
      bool,
    )
    or generator.decoration is not None
  ):
    return None

  return (
    expression,
  )


def render_toda_public_group_generator_latex(
  expression,
) -> str:
  eta_factors = (
    _toda_public_eta_composition_factors(
      expression
    )
  )

  if (
    eta_factors is not None
    and len(
      eta_factors
    ) >= 2
  ):
    indices = tuple(
      factor.generator.index
      for factor in eta_factors
    )
    start_index = indices[
      0
    ]

    if indices == tuple(
      range(
        start_index,
        start_index
        + len(
          eta_factors
        ),
      )
    ):
      return (
        r"\eta_{"
        + str(
          start_index
        )
        + r"}^{"
        + str(
          len(
            eta_factors
          )
        )
        + "}"
      )

  if isinstance(
    expression,
    Composition,
  ):
    left = expression.left
    right = expression.right

    if (
      isinstance(
        left,
        HomotopyElement,
      )
      and isinstance(
        right,
        HomotopyElement,
      )
    ):
      left_generator = (
        left.generator
      )
      right_generator = (
        right.generator
      )

      if (
        left_generator is not None
        and right_generator is not None
        and left_generator.family
        == "ν"
        and right_generator.family
        == "ν"
        and isinstance(
          left_generator.index,
          int,
        )
        and not isinstance(
          left_generator.index,
          bool,
        )
        and isinstance(
          right_generator.index,
          int,
        )
        and not isinstance(
          right_generator.index,
          bool,
        )
        and left_generator.decoration
        is None
        and right_generator.decoration
        is None
        and right_generator.index
        == left_generator.index + 3
      ):
        return (
          r"\nu_{"
          + str(
            left_generator.index
          )
          + r"}^{2}"
        )

  return (
    render_toda_expression_latex(
      expression
    )
  )
