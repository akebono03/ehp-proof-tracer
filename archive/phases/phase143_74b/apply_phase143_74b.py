from pathlib import Path
import ast

path = Path("toda_group_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
ast.parse(text)

old = """from homotopy_groups import (
  TodaDeltaMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
"""
new = """from homotopy_groups import (
  HomotopyEHPExactnessWindow,
  HomotopyGroup,
  TodaDeltaMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
"""
if old not in text:
  raise RuntimeError("homotopy_groups import anchor not found")
text = text.replace(old, new, 1)

old = """  TodaProp42ExactnessStatement,
  TodaProp51FiniteDimensionalStatement,
"""
new = """  TodaPi32Eta2DefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp51FiniteDimensionalStatement,
"""
if old not in text:
  raise RuntimeError("toda_rules import anchor not found")
text = text.replace(old, new, 1)

anchor = """  statement = proof_step.conclusion

  if isinstance(
    statement,
    TodaSuspensionMap,
  ):
"""
replacement = r"""  statement = proof_step.conclusion

  if isinstance(
    statement,
    HomotopyGroup,
  ):
    return (
      r"\pi_{"
      + _render_scalar_latex(
        statement.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement.sphere_dimension
      )
      + "}"
    )

  if isinstance(
    statement,
    HomotopyEHPExactnessWindow,
  ):
    return (
      r"\pi_{"
      + _render_scalar_latex(
        statement.source_term.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement.source_term.sphere_dimension
      )
      + r"} \xrightarrow{"
      + statement.first_map.name
      + r"} \pi_{"
      + _render_scalar_latex(
        statement.middle_term.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement.middle_term.sphere_dimension
      )
      + r"} \xrightarrow{"
      + statement.second_map.name
      + r"} \pi_{"
      + _render_scalar_latex(
        statement.target_term.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement.target_term.sphere_dimension
      )
      + "}"
    )

  if isinstance(
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

  if isinstance(
    statement,
    TodaPrimaryGroupMembershipStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.element
      )
      + r" \in "
      + render_toda_primary_group_latex(
        statement.group
      )
    )

  if isinstance(
    statement,
    TodaProp44IsomorphismStatement,
  ):
    return (
      r"\left("
      + render_toda_expression_latex(
        statement.map.beta
      )
      + r", "
      + render_toda_expression_latex(
        statement.map.gamma
      )
      + r"\right) \mapsto "
      + render_toda_expression_latex(
        statement.map.formula
      )
      + r"\quad\text{は同型写像}"
    )

  if isinstance(
    statement,
    TodaSuspensionIsomorphismStatement,
  ):
    return (
      r"E: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \xrightarrow{\cong} "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

  if isinstance(
    statement,
    TodaSuspensionMap,
  ):
"""
if anchor not in text:
  raise RuntimeError("latex insertion anchor not found")
text = text.replace(anchor, replacement, 1)

ast.parse(text)
path.write_text(text, encoding="utf-8", newline="\n")
print("Phase 143-74B implementation applied.")
print("Changed: toda_group_proof_narrative_renderer.py")
