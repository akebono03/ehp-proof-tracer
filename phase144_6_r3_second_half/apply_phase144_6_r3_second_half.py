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


def patch_toda_rules() -> None:
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
      node for node in ast.walk(function)
      if isinstance(node, ast.Call)
      and isinstance(node.func, ast.Name)
      and node.func.id == "InferenceRule"
    ]
    if len(calls) != 1:
      raise RuntimeError(
        f"{function_name}: expected one InferenceRule call, found {len(calls)}"
      )
    call = calls[0]
    if any(k.arg == "literature_reference" for k in call.keywords):
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
  anchor = '''from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
'''
  extra = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
'''
  if extra not in text:
    if anchor not in text:
      raise RuntimeError("multi renderer import anchor not found")
    text = text.replace(anchor, anchor + extra, 1)

  old = '''  return "\\n\\n".join(
    rendered_arguments
  )
'''
  new = '''  reference_entries = (
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
'''
  if new not in text:
    if text.count(old) != 1:
      raise RuntimeError("multi renderer return anchor mismatch")
    text = text.replace(old, new, 1)
  path.write_text(text, encoding="utf-8")


def write_tests() -> None:
  path = ROOT / "tests" / "test_phase144_6_r3_production_references.py"
  path.write_text('''from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _phase144_6_r3_pi6_3_data():
  report = build_standard_toda_report(n=3, k=3)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  return presentation, sidecar, blocks, arguments


def test_phase144_6_r3_pi6_3_references_are_structured_and_deduplicated():
  presentation, _, _, _ = _phase144_6_r3_pi6_3_data()
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  locators = tuple(entry.reference.locator for entry in entries)

  assert "(5.3) / Lemma 5.2" in locators
  assert "(5.2)" in locators
  assert "Proposition 4.4" in locators
  assert "Proposition 5.1" in locators
  assert locators.count("Proposition 4.4") == 1
  assert "Proposition 2.2" not in locators


def test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section():
  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()
  rendered = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )

  assert "使用する結果を先にまとめる." in rendered
  assert "(5.3) / Lemma 5.2" in rendered
  assert "(5.2)" in rendered
  assert "Proposition 4.4" in rendered
  assert "Proposition 5.1" in rendered
  assert "Proposition 2.2" not in rendered


def test_phase144_6_r3_reference_section_does_not_parse_internal_rule_names():
  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()
  rendered = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )
  reference_section = rendered.split("まず、", 1)[0]

  assert "eta_2 n=2 specialization" not in reference_section
  assert "finite-dimensional integration" not in reference_section
''', encoding="utf-8")


def main() -> int:
  patch_toda_rules()
  patch_multi_renderer()
  write_tests()
  print("Phase 144-6-R3 second half applied.")
  print("Changed: toda_rules.py")
  print("Changed: toda_group_proof_narrative_argument_multi_renderer.py")
  print("Added: tests/test_phase144_6_r3_production_references.py")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
