from pathlib import Path


PATH = Path("toda_proof_narrative_renderer.py")
BACKUP = Path(
  "toda_proof_narrative_renderer.py.phase143_75y_backup"
)


def _add_import(
  text: str,
) -> str:
  import_name = (
    "  TodaLemma54Nu4ConstructionStatement,\n"
  )

  if import_name in text:
    return text

  anchor = (
    "from toda_rules import (\n"
  )
  index = text.find(
    anchor
  )

  if index < 0:
    raise RuntimeError(
      "toda_rules import block not found"
    )

  insert_at = (
    index
    + len(anchor)
  )

  return (
    text[:insert_at]
    + import_name
    + text[insert_at:]
  )


def _add_helpers(
  text: str,
) -> str:
  marker = (
    "def render_toda_proof_statement_latex(\n"
    "  statement,\n"
    ") -> str | None:\n"
  )

  if (
    "def _render_toda_nu4_construction_branch_latex("
    in text
  ):
    return text

  index = text.find(
    marker
  )

  if index < 0:
    raise RuntimeError(
      "render_toda_proof_statement_latex "
      "function not found"
    )

  helpers = r'''def _render_toda_signed_expression_latex(
  sign: int,
  expression_latex: str,
) -> str | None:
  if sign == 1:
    return expression_latex

  if sign == -1:
    return (
      "-"
      + expression_latex
    )

  return None


def _render_toda_nu4_parameter_factor_latex(
  parameter,
  offset: int,
) -> str | None:
  if not isinstance(
    offset,
    int,
  ) or isinstance(
    offset,
    bool,
  ):
    return None

  parameter_latex = (
    _render_scalar_latex(
      parameter
    )
  )

  if offset == 0:
    return parameter_latex

  if offset > 0:
    return (
      r"\left("
      + parameter_latex
      + " + "
      + str(
        offset
      )
      + r"\right)"
    )

  return (
    r"\left("
    + parameter_latex
    + " - "
    + str(
      -offset
    )
    + r"\right)"
  )


def _render_toda_nu4_construction_branch_latex(
  statement,
  branch,
) -> str | None:
  alpha_latex = (
    render_toda_expression_latex(
      statement.alpha_star
    )
  )
  nu4_latex = (
    render_toda_expression_latex(
      statement.nu4
    )
  )
  whitehead_latex = (
    render_toda_expression_latex(
      statement.whitehead_data.whitehead_square
    )
  )
  sign_parameter_latex = (
    _render_scalar_latex(
      statement.whitehead_data.sign_parameter
    )
  )
  value_latex = (
    render_toda_expression_latex(
      statement.double_suspension_value
    )
  )

  alpha_term = (
    _render_toda_signed_expression_latex(
      branch.alpha_star_sign,
      alpha_latex,
    )
  )
  value_term = (
    _render_toda_signed_expression_latex(
      branch.double_suspension_sign,
      value_latex,
    )
  )
  parameter_factor = (
    _render_toda_nu4_parameter_factor_latex(
      statement.parameter,
      branch.parameter_offset,
    )
  )

  if (
    alpha_term is None
    or value_term is None
    or parameter_factor is None
    or branch.whitehead_coefficient_sign
    not in (
      -1,
      1,
    )
  ):
    return None

  whitehead_term = (
    r"(-1)^{"
    + sign_parameter_latex
    + "}"
    + parameter_factor
    + whitehead_latex
  )

  if (
    branch.whitehead_coefficient_sign
    == 1
  ):
    correction = (
      " + "
      + whitehead_term
    )
  else:
    correction = (
      " - "
      + whitehead_term
    )

  condition_latex = (
    r"2E"
    + alpha_latex
    + " = "
    + value_term
  )

  return (
    nu4_latex
    + " = "
    + alpha_term
    + correction
    + r" & \text{if } "
    + condition_latex
  )


'''

  return (
    text[:index]
    + helpers
    + text[index:]
  )


def _add_statement_branch(
  text: str,
) -> str:
  marker = (
    "def render_toda_proof_statement_latex(\n"
    "  statement,\n"
    ") -> str | None:\n"
  )

  branch = r'''  if isinstance(
    statement,
    TodaLemma54Nu4ConstructionStatement,
  ):
    positive_latex = (
      _render_toda_nu4_construction_branch_latex(
        statement,
        statement.positive_branch,
      )
    )
    negative_latex = (
      _render_toda_nu4_construction_branch_latex(
        statement,
        statement.negative_branch,
      )
    )

    if (
      positive_latex is None
      or negative_latex is None
    ):
      return None

    return (
      r"\begin{cases} "
      + positive_latex
      + r" \\ "
      + negative_latex
      + r" \end{cases}"
    )

'''

  if branch in text:
    return text

  index = text.find(
    marker
  )

  if index < 0:
    raise RuntimeError(
      "render_toda_proof_statement_latex "
      "function not found"
    )

  insert_at = (
    index
    + len(marker)
  )

  return (
    text[:insert_at]
    + branch
    + text[insert_at:]
  )


def main():
  text = PATH.read_text(
    encoding="utf-8"
  )

  if not BACKUP.exists():
    BACKUP.write_text(
      text,
      encoding="utf-8",
    )

  text = _add_import(
    text
  )
  text = _add_helpers(
    text
  )
  text = _add_statement_branch(
    text
  )

  PATH.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "Phase 143-75Y repair applied."
  )
  print(
    "Backup:",
    BACKUP,
  )


if __name__ == "__main__":
  main()
