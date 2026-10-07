def render_toda_group_structure_latex(
  group_structure: TodaGroupStructurePresentation,
) -> str:
  if not isinstance(
    group_structure,
    TodaGroupStructurePresentation,
  ):
    raise TypeError(
      "group_structure must be a "
      "TodaGroupStructurePresentation"
    )

  if (
    group_structure.kind
    is TodaGroupStructureKind.ZERO
  ):
    return "0"

  if (
    group_structure.kind
    is TodaGroupStructureKind.FREE_CYCLIC
  ):
    return (
      r"\mathbb{Z}\{"
      + render_toda_public_group_generator_latex(
        group_structure
        .generator
        .source_generator
      )
      + r"\}"
    )

  if (
    group_structure.kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  ):
    return (
      r"\mathbb{Z}/"
      + str(
        group_structure
        .generator
        .order
        .value
      )
      + r"\{"
      + render_toda_public_group_generator_latex(
        group_structure
        .generator
        .source_generator
      )
      + r"\}"
    )

  if (
    group_structure.kind
    is TodaGroupStructureKind.DIRECT_SUM
  ):
    return r" \oplus ".join(
      render_toda_group_structure_latex(
        summand
      )
      for summand in (
        group_structure.summands
      )
    )

  raise ValueError(
    "unsupported group structure kind"
  )
