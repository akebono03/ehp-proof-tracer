from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_repair9_final_public_reference_relink.py"
)

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

TEST_SOURCE = r'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_phase161_r4_r5_repair9_pi4_2() -> str:\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=3,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase161_r4_r5_repair9_final_public_relink_uses_prop51_on_pi4_3():\n  rendered = (\n    _render_phase161_r4_r5_repair9_pi4_2()\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert "**[R2] Proposition 5.1.**" in reference\n\n  assert (\n    r"\\pi_{n + 1}^{n} = "\n    r"\\mathbb{Z}/2\\{\\eta_{n}\\}"\n    in reference\n  )\n  assert (\n    r"\\pi_{n + 1}^{n} = "\n    r"\\mathbb{Z}/2\\{\\eta_{n}\\}"\n    not in body\n  )\n\n  pi4_3_paragraph = next(\n    paragraph\n    for paragraph in body.split(\n      "\\n\\n"\n    )\n    if (\n      r"\\pi_{4}^{3} = "\n      r"\\mathbb{Z}/2\\{\\eta_{3}\\}"\n      in paragraph\n    )\n  )\n\n  assert "[R2]" in pi4_3_paragraph\n  assert (\n    pi4_3_paragraph.count(\n      "[R2]"\n    )\n    == 1\n  )\n\n\ndef test_phase161_r4_r5_repair9_final_public_relink_keeps_pi4_2_contract():\n  rendered = (\n    _render_phase161_r4_r5_repair9_pi4_2()\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "Proposition 4.4" not in reference\n  assert "[R2]より, [R1]より" not in body\n\n  assert (\n    r"\\eta_{2}\\circ -: "\n    r"\\pi_{i}^{3} \\to \\pi_{i}^{2}"\n    in reference\n  )\n  assert "$i=4$" in body\n  assert (\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}"\n    in body\n  )\n  assert (\n    r"\\eta_{3} \\mapsto "\n    r"\\eta_{2}\\eta_{3}"\n    in body\n  )\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in body\n  )\n  assert "□" in body\n'


def _functions(
  source: str,
):
  tree = ast.parse(
    source
  )

  return {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }


def _replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing function: {function_name}"
    )

  node = functions[
    function_name
  ]
  lines = source.splitlines(
    keepends=True
  )
  replacement_lines = [
    line + "\n"
    for line in replacement.rstrip(
      "\n"
    ).split(
      "\n"
    )
  ]

  return "".join(
    lines[
      :node.lineno - 1
    ]
    + replacement_lines
    + lines[
      node.end_lineno:
    ]
  )


def _extract_function(
  source: str,
  function_name: str,
) -> str:
  node = _functions(
    source
  )[
    function_name
  ]
  lines = source.splitlines()

  return "\n".join(
    lines[
      node.lineno - 1:
      node.end_lineno
    ]
  ) + "\n"


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )

  function_name = (
    "render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown"
  )

  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      "Render function not found."
    )

  current_function = _extract_function(
    source,
    function_name,
  )

  old = """  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )

  reference_section = (
"""

  new = """  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )

  rendered = (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

  reference_section = (
"""

  if old not in current_function:
    raise RuntimeError(
      "Expected final render anchor not found."
    )

  updated_function = current_function.replace(
    old,
    new,
    1,
  )

  updated = _replace_function(
    source,
    function_name,
    updated_function,
  )

  ast.parse(
    updated
  )
  ast.parse(
    TEST_SOURCE
  )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP_DIR / TARGET.name,
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    OUTPUT_DIR
    / (
      "render_toda_group_proof_narrative_"
      "multi_argument_with_contributions_markdown.py.txt"
    )
  ).write_text(
    updated_function,
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_repair9_final_public_reference_relink.py.txt"
  ).write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    TARGET,
  )
  print(
    "Wrote:",
    TEST,
  )
  print(
    "Production imports changed: NONE"
  )
  print(
    "Added one final public Reference-body relink after filtering/restoration."
  )


if __name__ == "__main__":
  main()
