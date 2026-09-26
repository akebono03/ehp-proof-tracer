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


def statement_signature(statement):
  return (
    type(statement.alpha_star).__name__,
    render_value(statement.alpha_star),
    type(statement.parameter).__name__,
    render_value(statement.parameter),
    type(statement.generator).__name__,
    render_value(statement.generator),
  )


def equality_key(statement):
  try:
    hash(statement)
  except TypeError:
    return repr(statement)
  return statement


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

  identity_counts = Counter(
    id(statement)
    for statement in captured
  )

  equality_counts = Counter(
    equality_key(statement)
    for statement in captured
  )

  signature_counts = Counter(
    statement_signature(statement)
    for statement in captured
  )

  print("")
  print("=" * 78)
  print(
    "Phase 143-75AC-3 Hopf odd multiple "
    "dedup audit"
  )
  print("=" * 78)
  print(
    "raw renderer calls:",
    len(captured),
  )
  print(
    "unique object identities:",
    len(identity_counts),
  )
  print(
    "unique statement equalities:",
    len(equality_counts),
  )
  print(
    "unique field-value signatures:",
    len(signature_counts),
  )

  print("")
  print("Object identity call-count distribution")
  print("-" * 78)
  for call_count, object_count in sorted(
    Counter(
      identity_counts.values()
    ).items()
  ):
    print(
      f"{object_count} object(s) x "
      f"{call_count} renderer call(s)"
    )

  print("")
  print("Statement equality call-count distribution")
  print("-" * 78)
  for call_count, statement_count in sorted(
    Counter(
      equality_counts.values()
    ).items()
  ):
    print(
      f"{statement_count} equality class(es) x "
      f"{call_count} renderer call(s)"
    )

  print("")
  print("Field-value signature distribution")
  print("-" * 78)
  for signature, count in sorted(
    signature_counts.items(),
    key=lambda item: (
      -item[1],
      repr(item[0]),
    ),
  ):
    (
      alpha_type,
      alpha_latex,
      parameter_type,
      parameter_latex,
      generator_type,
      generator_latex,
    ) = signature

    print(f"{count} renderer call(s)")
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
  print("Cross-check")
  print("-" * 78)
  print(
    "The established Phase 143-75U inventory "
    "must still report exactly:"
  )
  print(
    "  TodaLemma54HopfOddMultipleStatement: "
    "20 occurrences, 18 groups"
  )
  print(
    "Do not equate raw renderer calls with "
    "fallback occurrences."
  )
  print("")
  print(
    "No source files were changed."
  )
  print(
    "No pytest was run."
  )


if __name__ == "__main__":
  main()
