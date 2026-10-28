def render_toda_expression_latex(
  expression,
) -> str:
  if isinstance(
    expression,
    Zero,
  ):
    return "0"

  if isinstance(
    expression,
    HomotopyElement,
  ):
    if expression.generator is not None:
      return (
        _render_generator_symbol_latex(
          expression.generator
        )
      )

    return (
      _render_unicode_math_name_latex(
        expression.name
      )
    )

  if isinstance(
    expression,
    Multiple,
  ):
    if expression.coefficient == -1:
      return (
        "-"
        + render_toda_expression_latex(
          expression.expression
        )
      )

    coefficient = (
      _render_scalar_latex(
        expression.coefficient
      )
    )

    return (
      coefficient
      + render_toda_expression_latex(
        expression.expression
      )
    )

  if isinstance(
    expression,
    Sum,
  ):
    left_latex = (
      render_toda_expression_latex(
        expression.left
      )
    )

    if (
      isinstance(
        expression.right,
        Multiple,
      )
      and isinstance(
        expression.right.coefficient,
        int,
      )
      and not isinstance(
        expression.right.coefficient,
        bool,
      )
      and expression.right.coefficient < 0
    ):
      magnitude = -expression.right.coefficient

      right_latex = (
        render_toda_expression_latex(
          expression.right.expression
        )
      )

      if magnitude != 1:
        right_latex = (
          str(
            magnitude
          )
          + right_latex
        )

      return (
        left_latex
        + " - "
        + right_latex
      )

    return (
      left_latex
      + " + "
      + render_toda_expression_latex(
        expression.right
      )
    )

  if isinstance(
    expression,
    SmashProduct,
  ):
    return (
      render_toda_expression_latex(
        expression.left
      )
      + r" \wedge "
      + render_toda_expression_latex(
        expression.right
      )
    )

  if isinstance(
    expression,
    WhiteheadProduct,
  ):
    return (
      "["
      + render_toda_expression_latex(
        expression.left
      )
      + ", "
      + render_toda_expression_latex(
        expression.right
      )
      + "]"
    )

  if isinstance(
    expression,
    Composition,
  ):
    from phase169_r10eb_typed_composition_power.display import (
      typed_stable_composition_power_latex,
    )
    power = typed_stable_composition_power_latex(expression)
    if power is not None:
      return power
    # Keep the legacy sigma fallback for historical non-canonical display names.
    # Compress only a well-typed consecutive sigma family composition.
    # This is a presentation rule: the Composition tree is unchanged.
    factors = []

    def collect_composition_factors(value):
      if isinstance(value, Composition):
        collect_composition_factors(value.left)
        collect_composition_factors(value.right)
      else:
        factors.append(value)

    collect_composition_factors(expression)
    if len(factors) >= 2:
      sigma_indices = []
      for factor in factors:
        if not isinstance(factor, HomotopyElement):
          break
        symbol = factor.generator
        if (
          symbol is None
          or symbol.family not in ("σ", r"\sigma")
          or type(symbol.index) is not int
          or factor.target != symbol.index
          or factor.source != symbol.index + 7
        ):
          break
        sigma_indices.append(symbol.index)
      if len(sigma_indices) == len(factors) and all(
        following == preceding + 7
        for preceding, following in zip(sigma_indices, sigma_indices[1:])
      ):
        return (
          render_toda_expression_latex(factors[0])
          + "^{" + str(len(factors)) + "}"
        )

    # A mixed composition can contain a consecutive typed power as one part.
    # Do not compress an ill-typed composite or infer equality from labels.
    if (
      len(factors) >= 3
      and all(isinstance(factor, HomotopyElement) for factor in factors)
      and all(
        type(left.source) is int
        and type(right.target) is int
        and left.source == right.target
        for left, right in zip(factors, factors[1:])
      )
    ):
      parts = []
      index = 0
      compressed = False
      while index < len(factors):
        end_of_run = index + 1
        run_latex = None
        for end in range(index + 2, len(factors) + 1):
          segment = factors[end - 1]
          for factor in reversed(factors[index:end - 1]):
            segment = Composition(factor, segment)
          candidate = typed_stable_composition_power_latex(segment)
          if candidate is not None:
            end_of_run = end
            run_latex = candidate
        if run_latex is None:
          parts.append(render_toda_expression_latex(factors[index]))
          index += 1
        else:
          parts.append(run_latex)
          index = end_of_run
          compressed = True
      if compressed:
        return "".join(parts)

    return (
      render_toda_expression_latex(
        expression.left
      )
      + render_toda_expression_latex(
        expression.right
      )
    )

  if isinstance(
    expression,
    MapApplication,
  ):
    return (
      _render_map_symbol_latex(
        expression.map
      )
      + r"\left("
      + render_toda_expression_latex(
        expression.expression
      )
      + r"\right)"
    )

  if isinstance(
    expression,
    Suspension,
  ):
    return (
      "E"
      + render_toda_expression_latex(
        expression.expression
      )
    )

  if isinstance(
    expression,
    IteratedSuspension,
  ):
    prefix = (
      "E"
      if type(expression.exponent) is int and expression.exponent == 1
      else "E^{" + _render_scalar_latex(expression.exponent) + "}"
    )
    return prefix + render_toda_expression_latex(expression.expression)

  if isinstance(
    expression,
    TodaBracket,
  ):
    latex = (
      r"\{"
      + render_toda_expression_latex(
        expression.first
      )
      + ", "
      + render_toda_expression_latex(
        expression.second
      )
      + ", "
      + render_toda_expression_latex(
        expression.third
      )
      + r"\}"
    )

    if expression.index is not None:
      latex += (
        "_{"
        + _render_scalar_latex(
          expression.index
        )
        + "}"
      )

    return latex

  raise TypeError(
    "unsupported expression for LaTeX rendering"
  )
