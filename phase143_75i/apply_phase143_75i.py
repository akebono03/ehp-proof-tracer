from pathlib import Path

path = Path(
  "toda_group_proof_narrative_renderer.py"
)
text = path.read_text(
  encoding="utf-8"
)

import_anchor = """  Toda56Nu4DecompositionStatement,
  TodaDeltaImageFreeCyclicStatement,
"""

import_replacement = """  Toda56Nu4DecompositionStatement,
  Toda58WhiteheadSquareUpToSignStatement,
  TodaDeltaImageFreeCyclicStatement,
"""

if import_anchor not in text:
  raise SystemExit(
    "Expected Toda rule import anchor "
    "was not found."
  )

text = text.replace(
  import_anchor,
  import_replacement,
  1,
)

import_anchor_2 = """  TodaPi32Eta2DefinitionStatement,
  TodaProp42ExactnessStatement,
"""

import_replacement_2 = """  TodaPi32Eta2DefinitionStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
"""

if import_anchor_2 not in text:
  raise SystemExit(
    "Expected pi_3^2 / Proposition 2.7 "
    "import anchor was not found."
  )

text = text.replace(
  import_anchor_2,
  import_replacement_2,
  1,
)

render_anchor = """  if isinstance(
    statement,
    TodaPi32Eta2DefinitionStatement,
  ):
    return (
      "H("
      + render_toda_expression_latex(
        statement.element
      )
      + ") = "
      + render_toda_expression_latex(
        statement.image
      )
    )

"""

render_addition = """  if isinstance(
    statement,
    (
      TodaPi32WhiteheadSquareUpToSignStatement,
      Toda58WhiteheadSquareUpToSignStatement,
    ),
  ):
    return (
      render_toda_expression_latex(
        statement.whitehead_square
      )
      + r" = \\pm "
      + render_toda_expression_latex(
        statement.positive_value
      )
    )

  if isinstance(
    statement,
    TodaProp27HopfInvariantUpToSignStatement,
  ):
    return (
      "H("
      + render_toda_expression_latex(
        statement.argument
      )
      + r") = \\pm "
      + render_toda_expression_latex(
        statement.positive_value
      )
    )

"""

if render_anchor not in text:
  raise SystemExit(
    "Expected eta_2 definition rendering "
    "anchor was not found."
  )

text = text.replace(
  render_anchor,
  render_anchor + render_addition,
  1,
)

path.write_text(
  text,
  encoding="utf-8",
)

print(
  "Phase 143-75I implementation applied."
)
print(
  "Changed: "
  "toda_group_proof_narrative_renderer.py"
)
