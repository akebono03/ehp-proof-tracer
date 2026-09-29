from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")
backup = path.with_suffix(path.suffix + ".phase143_75an_backup")
if not backup.exists():
  backup.write_text(text, encoding="utf-8")

tree = ast.parse(text)
import_node = next((
  node for node in tree.body
  if isinstance(node, ast.ImportFrom)
  and node.module == "toda_rules"
), None)
if import_node is None:
  raise RuntimeError("from toda_rules import block not found")

import_name = "Toda54IndeterminacyGeneratorStatement"
if not any(alias.name == import_name for alias in import_node.names):
  lines = text.splitlines(keepends=True)
  closing_index = import_node.end_lineno - 1
  if lines[closing_index].strip() != ")":
    raise RuntimeError("unexpected toda_rules import block ending")
  lines.insert(closing_index, "  " + import_name + ",\n")
  text = "".join(lines)

branch = """  if isinstance(
    statement,
    Toda54IndeterminacyGeneratorStatement,
  ):
    return (
      r"\\operatorname{Ind}\\left("
      + render_toda_expression_latex(
        statement.bracket
      )
      + r"\\right) = \\left\\langle "
      + render_toda_expression_latex(
        statement.generator
      )
      + r" \\right\\rangle"
    )

"""

if branch not in text:
  tree = ast.parse(text)
  target = next((
    node for node in tree.body
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    and node.name == "render_toda_proof_statement_latex"
  ), None)
  if target is None or not target.body:
    raise RuntimeError("render_toda_proof_statement_latex not found")
  lines = text.splitlines(keepends=True)
  lines.insert(target.body[0].lineno - 1, branch)
  text = "".join(lines)

ast.parse(text)
path.write_text(text, encoding="utf-8")
print("Phase 143-75AN semantic renderer patch applied.")
