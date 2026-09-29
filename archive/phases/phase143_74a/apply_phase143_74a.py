from pathlib import Path
import ast

path = Path("toda_group_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")
text = text.replace("\r\n", "\n")
ast.parse(text)

old_import = """from homotopy_groups import (
  TodaPrimaryGroup,
)
"""
new_import = """from homotopy_groups import (
  TodaDeltaMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
"""
if old_import not in text:
  raise RuntimeError("homotopy_groups import anchor not found")
text = text.replace(old_import, new_import, 1)

anchor = """  statement = proof_step.conclusion

  if isinstance(
    statement,
    ScalarGreaterEqualStatement,
  ):
"""
replacement = r"""  statement = proof_step.conclusion

  if isinstance(
    statement,
    TodaSuspensionMap,
  ):
    return (
      "E: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
    )

  if isinstance(
    statement,
    TodaIteratedSuspensionMap,
  ):
    return (
      r"E^{"
      + _render_scalar_latex(
        statement.exponent
      )
      + r"}: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
    )

  if isinstance(
    statement,
    TodaDeltaMap,
  ):
    return (
      r"\Delta: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
    )

  if isinstance(
    statement,
    TodaProp44DecompositionMap,
  ):
    return (
      r"("
      + render_toda_expression_latex(
        statement.beta
      )
      + r", "
      + render_toda_expression_latex(
        statement.gamma
      )
      + r") \mapsto "
      + render_toda_expression_latex(
        statement.formula
      )
    )

  if isinstance(
    statement,
    ScalarGreaterEqualStatement,
  ):
"""
if anchor not in text:
  raise RuntimeError("narrative latex insertion anchor not found")
text = text.replace(anchor, replacement, 1)

ast.parse(text)
path.write_text(text, encoding="utf-8", newline="\n")
print("Phase 143-74A implementation applied.")
print("Changed: toda_group_proof_narrative_renderer.py")
