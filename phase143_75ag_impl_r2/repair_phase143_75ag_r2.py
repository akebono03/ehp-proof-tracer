from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(
  path.suffix + ".phase143_75ag_r2_backup"
)
if not backup.exists():
  backup.write_text(
    text,
    encoding="utf-8",
  )

import_name = (
  "  TodaLemma510BracketModuloStatement,\n"
)

if import_name not in text:
  block_start = text.find(
    "from toda_rules import (\n"
  )
  if block_start == -1:
    raise RuntimeError(
      "from toda_rules import block not found"
    )

  block_end = text.find(
    "\n)\n",
    block_start,
  )
  if block_end == -1:
    raise RuntimeError(
      "end of toda_rules import block not found"
    )

  text = (
    text[:block_end]
    + "\n"
    + import_name.rstrip("\n")
    + text[block_end:]
  )

branch = (
  "  if isinstance(\n"
  "    statement,\n"
  "    TodaLemma510BracketModuloStatement,\n"
  "  ):\n"
  "    return (\n"
  "      render_toda_expression_latex(\n"
  "        statement.element\n"
  "      )\n"
  '      + r" \\\\in "\n'
  "      + render_toda_expression_latex(\n"
  "        statement.bracket\n"
  "      )\n"
  '      + r" \\\\pmod{"\n'
  "      + render_toda_scalar_latex(\n"
  "        statement.modulus\n"
  "      )\n"
  "      + render_toda_primary_group_latex(\n"
  "        statement.ambient_group\n"
  "      )\n"
  '      + r"}"\n'
  "    )\n"
  "\n"
)

if branch not in text:
  tree = ast.parse(text)

  target = None
  for node in tree.body:
    if (
      isinstance(
        node,
        (ast.FunctionDef, ast.AsyncFunctionDef),
      )
      and node.name
      == "render_toda_proof_statement_latex"
    ):
      target = node
      break

  if target is None:
    raise RuntimeError(
      "render_toda_proof_statement_latex "
      "not found"
    )

  lines = text.splitlines(keepends=True)

  if not target.body:
    raise RuntimeError(
      "render_toda_proof_statement_latex "
      "has no body"
    )

  first_body_line = target.body[0].lineno - 1
  lines.insert(
    first_body_line,
    branch,
  )
  text = "".join(lines)

ast.parse(text)

path.write_text(
  text,
  encoding="utf-8",
)

print(
  "Phase 143-75AG R2 semantic renderer "
  "patch applied."
)
print(
  "Insertion used the AST function boundary, "
  "not a neighboring statement anchor."
)
