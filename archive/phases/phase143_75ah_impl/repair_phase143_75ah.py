from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(
  path.suffix + ".phase143_75ah_backup"
)
if not backup.exists():
  backup.write_text(text, encoding="utf-8")

import_name = "  TodaLemma57TwoIota5ImageMembershipStatement,\n"

if import_name not in text:
  block_start = text.find("from toda_rules import (\n")
  if block_start == -1:
    raise RuntimeError("from toda_rules import block not found")

  block_end = text.find("\n)\n", block_start)
  if block_end == -1:
    raise RuntimeError("end of toda_rules import block not found")

  text = (
    text[:block_end]
    + "\n"
    + import_name.rstrip("\n")
    + text[block_end:]
  )

branch = """  if isinstance(
    statement,
    TodaLemma57TwoIota5ImageMembershipStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.element
      )
      + r" \\in 2\\iota_{5}\\circ "
      + render_toda_primary_group_latex(
        statement.source_group
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

print("Phase 143-75AH semantic renderer patch applied.")
print(
  "Reused existing statement semantics: "
  "element in 2 iota_5 composed with source_group."
)
