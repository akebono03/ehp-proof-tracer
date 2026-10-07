def _group_proof_statement_latex(
  statement,
) -> tuple[
  str | None,
  str | None,
]:
  public_group_latex = (
    render_toda_public_group_relation_latex(
      statement
    )
  )

  if public_group_latex is not None:
    return (
      public_group_latex,
      None,
    )

  try:
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = (
      render_toda_proof_statement_latex(
        statement
      )
    )

  if latex is None:
    return (
      None,
      type(
        statement
      ).__name__,
    )

  return (
    latex,
    None,
  )
