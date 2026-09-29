import runpy
from collections import Counter

import toda_proof_narrative_renderer as narrative
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_rules import (
  TodaLemma54HopfOddMultipleStatement,
)


TARGET_AUDIT = (
  "phase143_75u/"
  "audit_phase143_75u_remaining_fallbacks.py"
)


def render_value(value):
  try:
    return render_toda_expression_latex(value)
  except TypeError:
    try:
      return _render_scalar_latex(value)
    except TypeError:
      return repr(value)


def main():
  original = (
    narrative.render_toda_proof_statement_latex
  )
  captured = []

  def capturing_renderer(statement):
    if isinstance(
      statement,
      TodaLemma54HopfOddMultipleStatement,
    ):
      captured.append(statement)

    return original(statement)

  narrative.render_toda_proof_statement_latex = (
    capturing_renderer
  )

  try:
    runpy.run_path(
      TARGET_AUDIT,
      run_name="__main__",
    )
  finally:
    narrative.render_toda_proof_statement_latex = (
      original
    )

  signatures = Counter(
    (
      type(statement.alpha_star).__name__,
      render_value(statement.alpha_star),
      type(statement.parameter).__name__,
      render_value(statement.parameter),
      type(statement.generator).__name__,
      render_value(statement.generator),
    )
    for statement in captured
  )

  print("")
  print("=" * 78)
  print(
    "Phase 143-75AC-2 captured Hopf odd multiple "
    "field-value distribution"
  )
  print("=" * 78)
  print("captured renderer calls:", len(captured))
  print("distinct value signatures:", len(signatures))
  print("")

  for count, signature in sorted(
    (
      (count, signature)
      for signature, count in signatures.items()
    ),
    reverse=True,
  ):
    (
      alpha_type,
      alpha_latex,
      parameter_type,
      parameter_latex,
      generator_type,
      generator_latex,
    ) = signature

    print(f"{count} x")
    print(
      "  alpha_star: "
      f"{alpha_type}: {alpha_latex}"
    )
    print(
      "  parameter: "
      f"{parameter_type}: {parameter_latex}"
    )
    print(
      "  generator: "
      f"{generator_type}: {generator_latex}"
    )

  print("")
  print("Interpretation rule:")
  print(
    "  Do not implement the renderer until the captured "
    "population and value signatures have been inspected."
  )


if __name__ == "__main__":
  main()
