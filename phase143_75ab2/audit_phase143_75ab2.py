from collections import Counter, defaultdict
from dataclasses import fields

from test_phase60_nu4_whitehead_correction import (
  build_phase60_8_data,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaLemma54WhiteheadCorrectionDataStatement,
)


def _render_value(value):
  try:
    return render_toda_expression_latex(value)
  except Exception:
    return repr(value)


def main():
  statement = (
    build_phase60_8_data()[
      "whitehead_data_step"
    ].conclusion
  )

  print("=" * 78)
  print("Phase 143-75AB-2 Whitehead correction semantic structure audit")
  print("=" * 78)
  print("Focused canonical statement")
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
      f"{_render_value(value)}"
    )

  print(
    "current semantic rendering:",
    render_toda_proof_statement_latex(
      statement
    ),
  )

  print()
  print("=" * 78)
  print(
    "NOTE: the 112-group / 11033-node occurrence scan is supplied by "
    "the existing Phase 143 fallback audit below."
  )


if __name__ == "__main__":
  main()
