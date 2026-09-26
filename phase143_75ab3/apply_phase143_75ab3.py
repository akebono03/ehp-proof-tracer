from pathlib import Path

TARGET = Path("toda_proof_narrative_renderer.py")
TEST = Path("tests/test_phase143_75ab3_whitehead_correction_rendering.py")

text = TARGET.read_text(encoding="utf-8")

import_anchor = "from toda_rules import (\n"
start = text.find(import_anchor)
if start < 0:
  raise SystemExit("Could not locate toda_rules import block.")

end = text.find(")\n", start)
if end < 0:
  raise SystemExit("Could not locate end of toda_rules import block.")

import_block = text[start:end + 2]
import_name = "  TodaLemma54WhiteheadCorrectionDataStatement,\n"

if "TodaLemma54WhiteheadCorrectionDataStatement" not in import_block:
  import_block = import_block[:-2] + import_name + ")\n"
  text = text[:start] + import_block + text[end + 2:]

branch = r'''  if isinstance(
    statement,
    TodaLemma54WhiteheadCorrectionDataStatement,
  ):
    whitehead_square_latex = (
      render_toda_expression_latex(
        statement.whitehead_square
      )
    )

    return (
      r"H\left("
      + whitehead_square_latex
      + r"\right) = "
      + render_toda_expression_latex(
        statement.hopf_positive_value
      )
      + r",\quad "
      + _render_relation_latex(
        statement.suspension_zero_relation
      )
      + r",\quad "
      + render_toda_expression_latex(
        statement.sign_parameter
      )
      + r"\text{ is the sign parameter}"
    )

'''

function_start = text.find("def render_toda_proof_statement_latex(")
if function_start < 0:
  raise SystemExit("Could not locate render_toda_proof_statement_latex.")

literature_anchor = (
  "  if isinstance(\n"
  "    statement,\n"
  "    LiteratureStatement,\n"
  "  ):\n"
)
insert_at = text.find(literature_anchor, function_start)
if insert_at < 0:
  raise SystemExit("Could not locate LiteratureStatement branch.")

if "TodaLemma54WhiteheadCorrectionDataStatement" not in text[function_start:insert_at]:
  text = text[:insert_at] + branch + text[insert_at:]

backup = TARGET.with_suffix(TARGET.suffix + ".phase143_75ab3_backup")
if not backup.exists():
  backup.write_text(TARGET.read_text(encoding="utf-8"), encoding="utf-8")

TARGET.write_text(text, encoding="utf-8")

test_text = r'''from test_phase60_nu4_whitehead_correction import (
  build_phase60_8_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75ab3_renders_whitehead_correction_semantics():
  statement = (
    build_phase60_8_data()[
      "whitehead_data_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"H\left([\iota_{4}, \iota_{4}]\right) = 2\iota_{7},"
      r"\quad E\left([\iota_{4}, \iota_{4}]\right) = 0,"
      r"\quad u\text{ is the sign parameter}"
    )
  )


def test_phase143_75ab3_does_not_render_rule_name():
  statement = (
    build_phase60_8_data()[
      "whitehead_data_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert "Toda Lemma 5.4 Whitehead correction data" not in rendered


def test_phase143_75ab3_preserves_all_first_class_fields():
  statement = (
    build_phase60_8_data()[
      "whitehead_data_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert r"[\iota_{4}, \iota_{4}]" in rendered
  assert r"2\iota_{7}" in rendered
  assert r"E\left([\iota_{4}, \iota_{4}]\right) = 0" in rendered
  assert r"u\text{ is the sign parameter}" in rendered
'''

TEST.write_text(test_text, encoding="utf-8")
print("Phase 143-75AB-3 patch applied.")
