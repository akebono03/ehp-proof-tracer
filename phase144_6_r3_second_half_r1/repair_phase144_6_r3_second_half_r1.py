from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REFERENCE_BY_FUNCTION = {
  "toda_53_nu_prime_bracket_specialization_inference_rule":
    ("Toda (5.3) / Lemma 5.2", "(5.3) / Lemma 5.2"),
  "toda_52_eta2_composition_isomorphism_inference_rule":
    ("Toda (5.2)", "(5.2)"),
  "toda_prop44_eta2_n2_isomorphism_inference_rule":
    ("Toda Proposition 4.4", "Proposition 4.4"),
  "toda_prop44_eta2_second_summand_restriction_inference_rule":
    ("Toda Proposition 4.4", "Proposition 4.4"),
  "toda_prop51_finite_dimensional_integration_inference_rule":
    ("Toda Proposition 5.1", "Proposition 5.1"),
}


def _line_indent(line: str) -> str:
  return line[:len(line) - len(line.lstrip())]


def ensure_rule_references() -> None:
  path = ROOT / "toda_rules.py"
  text = path.read_text(encoding="utf-8-sig")

  import_line = "from proof import LiteratureReference\n"
  if import_line not in text:
    text = import_line + text

  tree = ast.parse(text)
  lines = text.splitlines(keepends=True)
  functions = {
    node.name: node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
  }
  insertions = []

  for function_name, (label, locator) in REFERENCE_BY_FUNCTION.items():
    function = functions.get(function_name)
    if function is None:
      raise RuntimeError(f"missing function: {function_name}")

    calls = [
      node
      for node in ast.walk(function)
      if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "InferenceRule"
      )
    ]
    if len(calls) != 1:
      raise RuntimeError(
        f"{function_name}: expected one InferenceRule call, "
        f"found {len(calls)}"
      )

    call = calls[0]
    if any(
      keyword.arg == "literature_reference"
      for keyword in call.keywords
    ):
      continue

    closing_index = call.end_lineno - 1
    indent = _line_indent(lines[closing_index]) + "  "
    insertion = (
      f'{indent}literature_reference=LiteratureReference(\n'
      f'{indent}  label="{label}",\n'
      f'{indent}  author="H. Toda",\n'
      f'{indent}  title="Composition Methods in Homotopy Groups of Spheres",\n'
      f'{indent}  year=1962,\n'
      f'{indent}  locator="{locator}",\n'
      f'{indent}),\n'
    )
    insertions.append((closing_index, insertion))

  for index, insertion in sorted(insertions, reverse=True):
    lines.insert(index, insertion)

  path.write_text("".join(lines), encoding="utf-8")


def patch_multi_renderer() -> None:
  path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
  text = path.read_text(encoding="utf-8-sig")

  import_anchor = """from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
"""
  reference_import = """from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
"""

  if reference_import not in text:
    if import_anchor not in text:
      raise RuntimeError("multi renderer import anchor not found")
    text = text.replace(
      import_anchor,
      import_anchor + reference_import,
      1,
    )

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

  already_connected = any(
    isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id
    == "build_toda_group_proof_narrative_reference_entries"
    for node in ast.walk(function)
  )
  if already_connected:
    path.write_text(text, encoding="utf-8")
    return

  return_nodes = [
    node
    for node in ast.walk(function)
    if isinstance(node, ast.Return)
  ]
  if len(return_nodes) != 1:
    raise RuntimeError(
      "expected exactly one return in multi renderer function"
    )

  return_node = return_nodes[0]
  lines = text.splitlines(keepends=True)
  start = return_node.lineno - 1
  end = return_node.end_lineno

  replacement = """  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries
    )
  )

  parts = tuple(
    part
    for part in (
      reference_section,
      "\\n\\n".join(
        rendered_arguments
      ),
    )
    if part
  )

  return "\\n\\n".join(
    parts
  )
"""

  lines[start:end] = [replacement]
  path.write_text("".join(lines), encoding="utf-8")


def main() -> int:
  ensure_rule_references()
  patch_multi_renderer()
  print("Phase 144-6-R3 second-half R1 repair applied.")
  print("Ensured: toda_rules.py structured references")
  print("Repaired: toda_group_proof_narrative_argument_multi_renderer.py")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
