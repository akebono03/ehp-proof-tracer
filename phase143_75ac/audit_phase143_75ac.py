from dataclasses import fields

from test_phase60_toda48_hopf_parity import (
  build_phase60_7_data,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
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
  statement = (
    build_phase60_7_data()[
      "final_step"
    ].conclusion
  )

  print("=" * 78)
  print("Phase 143-75AC Hopf odd multiple semantic structure audit")
  print("=" * 78)
  print("Canonical statement")
  print("-" * 78)
  print("type:", type(statement).__name__)
  print(
    "fields:",
    tuple(
      field.name
      for field in fields(statement)
    ),
  )

  for field in fields(statement):
    value = getattr(
      statement,
      field.name,
    )
    print(
      f"{field.name}: "
      f"{type(value).__name__}: "
      f"{render_value(value)}"
    )

  print(
    "current semantic rendering:",
    render_toda_proof_statement_latex(
      statement
    ),
  )


if __name__ == "__main__":
  main()
