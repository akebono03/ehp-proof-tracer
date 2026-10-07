def render_toda_public_group_relation_latex(
  statement,
) -> str | None:
  from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
  )
  from proof import (
    Relation,
    RelationType,
  )

  if isinstance(
    statement,
    TodaPrimaryGroupZeroStatement,
  ):
    return (
      r"\pi_{"
      + _render_scalar_latex(
        statement
        .group
        .group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement
        .group
        .sphere_dimension
      )
      + "} = 0"
    )

  if (
    not isinstance(
      statement,
      Relation,
    )
    or statement.relation_type
    is not RelationType.EQUALITY
    or not isinstance(
      statement.lhs,
      TodaPrimaryGroup,
    )
    or not isinstance(
      statement.rhs,
      (
        FreeCyclicGroup,
        FiniteCyclicGroup,
        DirectSumGroup,
      ),
    )
  ):
    return None

  def render_group_structure(
    group_structure,
  ) -> str:
    if isinstance(
      group_structure,
      FreeCyclicGroup,
    ):
      return (
        r"\mathbb{Z}\{"
        + render_toda_public_group_generator_latex(
          group_structure.generator
        )
        + r"\}"
      )

    if isinstance(
      group_structure,
      FiniteCyclicGroup,
    ):
      return (
        r"\mathbb{Z}/"
        + str(
          group_structure.order
        )
        + r"\{"
        + render_toda_public_group_generator_latex(
          group_structure.generator
        )
        + r"\}"
      )

    if isinstance(
      group_structure,
      DirectSumGroup,
    ):
      return r" \oplus ".join(
        render_group_structure(
          summand
        )
        for summand in (
          group_structure.summands
        )
      )

    raise ValueError(
      "unsupported public group structure"
    )

  return (
    r"\pi_{"
    + _render_scalar_latex(
      statement.lhs.group_dimension
    )
    + r"}^{"
    + _render_scalar_latex(
      statement.lhs.sphere_dimension
    )
    + "} = "
    + render_group_structure(
      statement.rhs
    )
  )
