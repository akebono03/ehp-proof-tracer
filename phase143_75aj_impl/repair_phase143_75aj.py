from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(
  path.suffix + ".phase143_75aj_backup"
)
if not backup.exists():
  backup.write_text(text, encoding="utf-8")

required_imports = (
  "  Toda36Lemma54SpecializationStatement,\n",
  "  TodaBracketMembershipStatement,\n",
)

block_start = text.find("from toda_rules import (\n")
if block_start == -1:
  raise RuntimeError("from toda_rules import block not found")

block_end = text.find("\n)\n", block_start)
if block_end == -1:
  raise RuntimeError("end of toda_rules import block not found")

for import_line in required_imports:
  if import_line not in text:
    text = (
      text[:block_end]
      + "\n"
      + import_line.rstrip("\n")
      + text[block_end:]
    )
    block_end = text.find("\n)\n", block_start)

helper = """def _render_homotopy_group_membership_latex(
  statement: HomotopyGroupMembershipStatement,
) -> str:
  return (
    render_toda_expression_latex(
      statement.element
    )
    + r" \\in \\pi_{"
    + _render_scalar_latex(
      statement.group_dimension
    )
    + "}^{"
    + _render_scalar_latex(
      statement.sphere_dimension
    )
    + "}"
  )


def _render_toda_bracket_membership_latex(
  statement: TodaBracketMembershipStatement,
) -> str:
  return (
    render_toda_expression_latex(
      statement.element
    )
    + r" \\in "
    + render_toda_expression_latex(
      statement.bracket
    )
  )


"""

if "def _render_homotopy_group_membership_latex(" not in text:
  marker = "def render_toda_proof_statement_latex("
  marker_index = text.find(marker)
  if marker_index == -1:
    raise RuntimeError(
      "render_toda_proof_statement_latex not found"
    )
  text = text[:marker_index] + helper + text[marker_index:]

branch = """  if isinstance(
    statement,
    Toda36Lemma54SpecializationStatement,
  ):
    return (
      _render_homotopy_group_membership_latex(
        statement.alpha_star_membership
      )
      + r", \\qquad "
      + _render_toda_bracket_membership_latex(
        statement.negative_bracket_membership
      )
    )

"""

if branch not in text:
  tree = ast.parse(text)
  target = next(
    (
      node
      for node in tree.body
      if isinstance(
        node,
        (ast.FunctionDef, ast.AsyncFunctionDef),
      )
      and node.name == "render_toda_proof_statement_latex"
    ),
    None,
  )
  if target is None or not target.body:
    raise RuntimeError(
      "render_toda_proof_statement_latex not found"
    )

  lines = text.splitlines(keepends=True)
  lines.insert(target.body[0].lineno - 1, branch)
  text = "".join(lines)

ast.parse(text)
path.write_text(text, encoding="utf-8")
print("Phase 143-75AJ semantic renderer patch applied.")
