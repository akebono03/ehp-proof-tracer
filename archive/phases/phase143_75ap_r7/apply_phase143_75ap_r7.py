from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")
tree = ast.parse(text)

targets = []

for node in ast.walk(tree):
  if not isinstance(node, ast.Call):
    continue

  if not (
    isinstance(node.func, ast.Name)
    and node.func.id
    == "render_toda_expression_latex"
  ):
    continue

  if len(node.args) != 1:
    continue

  arg = node.args[0]

  if not (
    isinstance(arg, ast.Attribute)
    and arg.attr == "hopf_relation"
    and isinstance(arg.value, ast.Name)
    and arg.value.id == "statement"
  ):
    continue

  targets.append(node.func)

if len(targets) != 1:
  raise RuntimeError(
    "Expected exactly one AST call rendering "
    "statement.hopf_relation with "
    "render_toda_expression_latex; "
    f"found {len(targets)}."
  )

target = targets[0]
lines = text.splitlines(keepends=True)
line_index = target.lineno - 1
line = lines[line_index]

start = target.col_offset
end = getattr(
  target,
  "end_col_offset",
  start + len("render_toda_expression_latex"),
)

if line[start:end] != "render_toda_expression_latex":
  raise RuntimeError(
    "AST target source did not match expected "
    "renderer name."
  )

lines[line_index] = (
  line[:start]
  + "_render_relation_latex"
  + line[end:]
)

text = "".join(lines)
ast.parse(text)

path.write_text(
  text,
  encoding="utf-8",
)

print(
  "Phase 143-75AP R7 relation rendering "
  "repair applied."
)
