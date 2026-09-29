from pathlib import Path
import subprocess

repo = Path.cwd()
renderer = repo / "toda_group_proof_narrative_renderer.py"
test = repo / "tests" / "test_phase143_73a_internal_statement_narrative.py"

original = subprocess.check_output(
    [
        "git",
        "show",
        "HEAD:toda_group_proof_narrative_renderer.py",
    ],
    cwd=repo,
).decode("utf-8")

text = original

repository_import = """from repository_element_presentation import (
  render_repository_conclusion_latex,
)
"""
scalar_import = """from scalar_rules import (
  ScalarGreaterEqualStatement,
)
"""

if scalar_import not in text:
    if repository_import not in text:
        raise RuntimeError("repository import anchor not found")
    text = text.replace(
        repository_import,
        scalar_import + repository_import,
        1,
    )

toda_anchor = "  TodaDeltaZeroStatement,\n"
eta_import = "  TodaEtaFamilyDefinitionStatement,\n"
if eta_import not in text:
    if toda_anchor not in text:
        raise RuntimeError("Toda import anchor not found")
    text = text.replace(
        toda_anchor,
        toda_anchor + eta_import,
        1,
    )

label_anchor = """  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return "\u03c3-family \u306e\u5b9a\u7fa9"

  return None
"""
label_replacement = """  if isinstance(
    statement,
    TodaEtaFamilyDefinitionStatement,
  ):
    return "\u03b7-family \u306e\u5b9a\u7fa9"

  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return "\u03c3-family \u306e\u5b9a\u7fa9"

  return None
"""
if label_anchor not in text:
    raise RuntimeError("Narrative label anchor not found")
text = text.replace(
    label_anchor,
    label_replacement,
    1,
)

latex_anchor = """  statement = proof_step.conclusion

  try:
"""
latex_replacement = """  statement = proof_step.conclusion

  if isinstance(
    statement,
    ScalarGreaterEqualStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.left
      )
      + r" \\ge "
      + render_toda_expression_latex(
        statement.right
      )
    )

  try:
"""
if latex_anchor not in text:
    raise RuntimeError("Narrative LaTeX anchor not found")
text = text.replace(
    latex_anchor,
    latex_replacement,
    1,
)

renderer.write_text(
    text,
    encoding="utf-8",
    newline="\n",
)

test_text = """from expression import (
  ScalarSymbol,
)
from proof import (
  ProofRule,
  ProofStep,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_rules import (
  toda_eta_family_definition_statement,
)


def test_phase143_73a_scalar_greater_equal_statement_renders_as_latex():
  n = ScalarSymbol(
    name="n",
  )

  step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    _render_group_proof_narrative_fact(
      step
    )
    == r"$n \\ge 5$"
  )


def test_phase143_73a_eta_family_definition_uses_human_readable_label():
  n = ScalarSymbol(
    name="n",
  )

  step = ProofStep(
    conclusion=(
      toda_eta_family_definition_statement(
        n
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    _render_group_proof_narrative_fact(
      step
    )
    == "\\u03b7-family \\u306e\\u5b9a\\u7fa9"
  )
"""

test.write_text(
    test_text,
    encoding="utf-8",
    newline="\n",
)

print("Phase 143-73A R3 repair applied.")
print("Restored renderer from git HEAD before applying the two 73A changes.")
print("Changed: toda_group_proof_narrative_renderer.py")
print("Added:   tests/test_phase143_73a_internal_statement_narrative.py")
