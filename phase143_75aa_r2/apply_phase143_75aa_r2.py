from pathlib import Path
import shutil

TARGET = Path("toda_proof_narrative_renderer.py")
TEST = Path("tests/test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py")

if not TARGET.exists():
    raise SystemExit("Could not find toda_proof_narrative_renderer.py. Run from repository root.")

source = TARGET.read_text(encoding="utf-8")
backup = TARGET.with_suffix(TARGET.suffix + ".phase143_75aa_r2_backup")
if not backup.exists():
    shutil.copy2(TARGET, backup)

import_name = "  Toda56Nu4Prop44SpecializationStatement,\n"
if import_name not in source:
    marker = "from toda_rules import (\n"
    start = source.find(marker)
    if start < 0:
        raise SystemExit("Could not find toda_rules import block.")
    close = source.find(")\n", start + len(marker))
    if close < 0:
        raise SystemExit("Could not find end of toda_rules import block.")
    source = source[:close] + import_name + source[close:]

branch = """  if isinstance(
    statement,
    Toda56Nu4Prop44SpecializationStatement,
  ):
    membership = statement.membership

    membership_latex = (
      render_toda_expression_latex(
        membership.element
      )
      + r" \\in "
      + render_toda_primary_group_latex(
        membership.group
      )
    )

    return (
      "n = "
      + _render_scalar_latex(
        statement.n
      )
      + r",\\quad \\alpha = "
      + render_toda_expression_latex(
        statement.alpha
      )
      + r",\\quad "
      + membership_latex
      + r",\\quad "
      + _render_relation_latex(
        statement.hopf_relation
      )
    )

"""

branch_signature = """  if isinstance(
    statement,
    Toda56Nu4Prop44SpecializationStatement,
  ):
"""
if branch_signature not in source:
    marker = """  if isinstance(
    statement,
    LiteratureStatement,
  ):
"""
    function_start = source.find("def render_toda_proof_statement_latex(")
    pos = source.find(marker, function_start)
    if pos < 0:
        raise SystemExit("Could not find LiteratureStatement branch in render_toda_proof_statement_latex.")
    source = source[:pos] + branch + source[pos:]

TARGET.write_text(source, encoding="utf-8")

test_source = """from test_phase63_nu4_prop44_specialization import (
  build_phase63_2_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75aa_renders_specialization_semantics():
  statement = (
    build_phase63_2_data()[
      "specialization_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"n = 4,\\quad \\alpha = \\nu_{4},"
      r"\\quad \\nu_{4} \\in \\pi_{7}^{4},"
      r"\\quad H\\left(\\nu_{4}\\right) = \\iota_{7}"
    )
  )


def test_phase143_75aa_does_not_render_rule_name():
  statement = (
    build_phase63_2_data()[
      "specialization_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert "Proposition 4.4 specialization premises" not in rendered
  assert "Toda (5.6)" not in rendered


def test_phase143_75aa_does_not_expand_lemma54_statement():
  statement = (
    build_phase63_2_data()[
      "specialization_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert r"E^{2}\\nu_{4}" not in rendered
  assert r"\\Delta" not in rendered
  assert rendered.count(r"\\nu_{4}") == 3
"""
TEST.write_text(test_source, encoding="utf-8")
print("Phase 143-75AA-R2 patch applied.")
