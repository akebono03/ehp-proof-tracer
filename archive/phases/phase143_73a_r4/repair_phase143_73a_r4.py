from pathlib import Path
import ast
import subprocess

repo = Path.cwd()
renderer = repo / "toda_group_proof_narrative_renderer.py"
test = repo / "tests" / "test_phase143_73a_internal_statement_narrative.py"

raw = subprocess.check_output(
    [
        "git",
        "show",
        "HEAD:toda_group_proof_narrative_renderer.py",
    ],
    cwd=repo,
)

original = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")

ast.parse(
    original,
    filename="HEAD:toda_group_proof_narrative_renderer.py",
)

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
        raise RuntimeError(
            "repository import anchor not found after newline normalization"
        )
    text = text.replace(
        repository_import,
        scalar_import + repository_import,
        1,
    )

toda_anchor = "  TodaDeltaZeroStatement,\n"
eta_import = "  TodaEtaFamilyDefinitionStatement,\n"

if eta_import not in text:
    if toda_anchor not in text:
        raise RuntimeError(
            "TodaDeltaZeroStatement import anchor not found"
        )
    text = text.replace(
        toda_anchor,
        toda_anchor + eta_import,
        1,
    )

sigma_label = (
    "  if isinstance(\n"
    "    statement,\n"
    "    TodaSigmaFamilyDefinitionStatement,\n"
    "  ):\n"
    '    return "\u03c3-family \u306e\u5b9a\u7fa9"\n'
    "\n"
    "  return None\n"
)

eta_and_sigma_label = (
    "  if isinstance(\n"
    "    statement,\n"
    "    TodaEtaFamilyDefinitionStatement,\n"
    "  ):\n"
    '    return "\u03b7-family \u306e\u5b9a\u7fa9"\n'
    "\n"
    "  if isinstance(\n"
    "    statement,\n"
    "    TodaSigmaFamilyDefinitionStatement,\n"
    "  ):\n"
    '    return "\u03c3-family \u306e\u5b9a\u7fa9"\n'
    "\n"
    "  return None\n"
)

if sigma_label not in text:
    raise RuntimeError(
        "sigma-family label anchor not found"
    )

text = text.replace(
    sigma_label,
    eta_and_sigma_label,
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
    raise RuntimeError(
        "Narrative LaTeX anchor not found"
    )

text = text.replace(
    latex_anchor,
    latex_replacement,
    1,
)

ast.parse(
    text,
    filename="toda_group_proof_narrative_renderer.py",
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

ast.parse(
    test_text,
    filename="test_phase143_73a_internal_statement_narrative.py",
)

test.write_text(
    test_text,
    encoding="utf-8",
    newline="\n",
)

print("Phase 143-73A R4 repair applied.")
print("Restored toda_group_proof_narrative_renderer.py from git HEAD.")
print("Normalized CRLF/LF before applying Phase 143-73A.")
print("Changed: toda_group_proof_narrative_renderer.py")
print("Added:   tests/test_phase143_73a_internal_statement_narrative.py")
