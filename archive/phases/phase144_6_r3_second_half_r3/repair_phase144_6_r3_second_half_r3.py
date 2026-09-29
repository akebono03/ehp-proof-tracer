from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def patch_multi_renderer() -> None:
  path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
  text = path.read_text(encoding="utf-8-sig")
  tree = ast.parse(text)

  function = next(
    (
      node
      for node in tree.body
      if (
        isinstance(node, ast.FunctionDef)
        and node.name
        == "render_toda_group_proof_narrative_multi_argument_markdown"
      )
    ),
    None,
  )
  if function is None:
    raise RuntimeError("multi renderer function not found")

  returns = [
    node
    for node in ast.walk(function)
    if isinstance(node, ast.Return)
  ]
  if len(returns) != 1:
    raise RuntimeError(
      f"expected exactly one return, found {len(returns)}"
    )

  return_node = returns[0]

  already_numbered = (
    isinstance(return_node.value, ast.Call)
    and isinstance(return_node.value.func, ast.Name)
    and return_node.value.func.id
    == "number_toda_group_proof_narrative_equations"
  )
  if already_numbered:
    print("Equation numbering finalizer already present.")
    return

  expected_join = (
    isinstance(return_node.value, ast.Call)
    and isinstance(return_node.value.func, ast.Attribute)
    and return_node.value.func.attr == "join"
  )
  if not expected_join:
    raise RuntimeError(
      "unexpected final return shape; refusing to patch"
    )

  lines = text.splitlines(keepends=True)
  start = return_node.lineno - 1
  end = return_node.end_lineno

  replacement = (
    '  return number_toda_group_proof_narrative_equations(\n'
    '    "\\n\\n".join(\n'
    '      parts\n'
    '    ),\n'
    '    presentation,\n'
    '    blocks,\n'
    '  )\n'
  )

  lines[start:end] = [replacement]
  path.write_text("".join(lines), encoding="utf-8")


def main() -> int:
  patch_multi_renderer()
  print("Phase 144-6-R3 second-half R3 equation-numbering repair applied.")
  print(
    "Changed only: "
    "toda_group_proof_narrative_argument_multi_renderer.py"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
