from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")
tree = ast.parse(text)

def attribute_chain(node):
  parts = []
  current = node

  while isinstance(current, ast.Attribute):
    parts.append(current.attr)
    current = current.value

  if isinstance(current, ast.Name):
    parts.append(current.id)
    return tuple(reversed(parts))

  return None


replacements = {
  (
    "statement",
    "prop44_isomorphism",
    "map",
    "target_group",
  ): "_render_phase143_75ao_homotopy_group",
  (
    "statement",
    "transported_group",
  ): "render_toda_raw_group_structure_latex",
}

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

  chain = attribute_chain(node.args[0])

  if chain in replacements:
    targets.append(
      (
        node.func,
        chain,
        replacements[chain],
      )
    )

found_chains = [
  chain
  for _, chain, _ in targets
]

for expected in replacements:
  count = found_chains.count(expected)

  if count != 1:
    raise RuntimeError(
      "Expected exactly one AST call for "
      f"{'.'.join(expected)}; found {count}."
    )

lines = text.splitlines(keepends=True)

for target, chain, replacement in sorted(
  targets,
  key=lambda item: (
    item[0].lineno,
    item[0].col_offset,
  ),
  reverse=True,
):
  line_index = target.lineno - 1
  line = lines[line_index]

  start = target.col_offset
  end = getattr(
    target,
    "end_col_offset",
    start + len(
      "render_toda_expression_latex"
    ),
  )

  if (
    line[start:end]
    != "render_toda_expression_latex"
  ):
    raise RuntimeError(
      "AST target source did not match "
      f"for {'.'.join(chain)}."
    )

  lines[line_index] = (
    line[:start]
    + replacement
    + line[end:]
  )

text = "".join(lines)
ast.parse(text)

path.write_text(
  text,
  encoding="utf-8",
)

print(
  "Phase 143-75AP R8 transported-decomposition "
  "group rendering repair applied."
)
