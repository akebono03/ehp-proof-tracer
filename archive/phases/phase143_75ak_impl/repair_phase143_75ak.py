from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(
  path.suffix + ".phase143_75ak_backup"
)
if not backup.exists():
  backup.write_text(text, encoding="utf-8")

import_line = "  TodaLemma514SigmaDoublePrimeStatement,\\n"

block_start = text.find("from toda_rules import (\\n")
if block_start == -1:
  raise RuntimeError("from toda_rules import block not found")

block_end = text.find("\\n)\\n", block_start)
if block_end == -1:
  raise RuntimeError("end of toda_rules import block not found")

if import_line not in text:
  text = (
    text[:block_end]
    + "\\n"
    + import_line.rstrip("\\n")
    + text[block_end:]
  )

branch = '''  if isinstance(
    statement,
    TodaLemma514SigmaDoublePrimeStatement,
  ):
    return (
      _render_relation_latex(
        statement.iterated_suspension_relation
      )
      + r", \\qquad "
      + _render_relation_latex(
        statement.double_relation
      )
      + r", \\qquad "
      + _render_relation_latex(
        statement.hopf_relation
      )
    )

'''

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
print("Phase 143-75AK semantic renderer patch applied.")
