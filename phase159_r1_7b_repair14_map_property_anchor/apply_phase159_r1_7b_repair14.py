from __future__ import annotations

import ast
from pathlib import Path
import shutil


ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_7b_repair14_map_property_anchor.py"
BACKUP_DIR = ROOT / "phase159_r1_7b_repair14_backup_before_apply"

NEW_FUNCTION = 'def _phase159_r1_7b_normalize_public_exact_sequences(\n  presentation: TodaGroupProofPresentation,\n  proof_body: list[\n    str\n  ],\n) -> list[\n  str\n]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    proof_body,\n    list,\n  ):\n    raise TypeError(\n      "proof_body must be a list"\n    )\n\n  semantic_presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  exactness_latex = tuple(\n    latex\n    for latex in (\n      _phase159_r1_7b_exactness_step_latex(\n        node.proof_step\n      )\n      for node in semantic_presentation.nodes\n    )\n    if latex is not None\n  )\n\n  lines = []\n\n  for line in proof_body:\n    inline_exactness = (\n      _phase159_r1_7b_inline_exactness_latex(\n        line\n      )\n    )\n\n    if inline_exactness is not None:\n      lines.extend(\n        _phase159_r1_7b_display_math_lines(\n          inline_exactness\n        )\n      )\n      continue\n\n    inline_short_exact = (\n      _phase159_r1_7b_inline_short_exact_latex(\n        line\n      )\n    )\n\n    if inline_short_exact is not None:\n      lines.extend(\n        _phase159_r1_7b_display_math_lines(\n          inline_short_exact\n        )\n      )\n      continue\n\n    lines.append(\n      line\n    )\n\n  line_index = 0\n\n  while line_index < len(\n    lines\n  ):\n    signature = (\n      _phase159_r1_7b_map_property_signature(\n        lines[\n          line_index\n        ]\n      )\n    )\n\n    if signature is None:\n      line_index += 1\n      continue\n\n    matching_latex = next(\n      (\n        latex\n        for latex in exactness_latex\n        if (\n          _phase159_r1_7b_exactness_matches_map_property(\n            latex,\n            signature,\n          )\n        )\n      ),\n      None,\n    )\n\n    if matching_latex is None:\n      line_index += 1\n      continue\n\n    existing_span = (\n      _phase159_r1_7b_find_display_math_span(\n        lines,\n        matching_latex,\n      )\n    )\n\n    if (\n      existing_span is not None\n      and existing_span[\n        0\n      ] < line_index\n    ):\n      line_index += 1\n      continue\n\n    if existing_span is not None:\n      span_start, span_end = existing_span\n\n      del lines[\n        span_start:span_end\n      ]\n\n      if span_start < line_index:\n        line_index -= (\n          span_end\n          - span_start\n        )\n\n    display_lines = list(\n      _phase159_r1_7b_display_math_lines(\n        matching_latex\n      )\n    )\n\n    lines[\n      line_index:line_index\n    ] = display_lines\n\n    line_index += (\n      len(\n        display_lines\n      )\n      + 1\n    )\n\n  return lines\n'
TEST_CONTENT = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi11_4() -> str:\n  report = build_standard_toda_report(\n    n=4,\n    k=7,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_7b_repair14_exactness_precedes_visible_delta_property():\n  rendered = _render_pi11_4()\n\n  exactness = (\n    "\\\\[\\n"\n    r"\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} "\n    r"\\xrightarrow{\\Delta} \\pi_{8}^{2}."\n    "\\n\\\\]"\n  )\n  surjectivity = (\n    r"$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$"\n    " は全射."\n  )\n\n  assert exactness in rendered\n  assert surjectivity in rendered\n  assert rendered.index(\n    exactness\n  ) < rendered.index(\n    surjectivity\n  )\n\n\ndef test_phase159_r1_7b_repair14_matching_exactness_is_not_duplicated():\n  rendered = _render_pi11_4()\n\n  exactness = (\n    "\\\\[\\n"\n    r"\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} "\n    r"\\xrightarrow{\\Delta} \\pi_{8}^{2}."\n    "\\n\\\\]"\n  )\n\n  assert rendered.count(\n    exactness\n  ) == 1\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )

  target = next(
    (
      node
      for node in tree.body
      if (
        isinstance(
          node,
          ast.FunctionDef,
        )
        and node.name
        == function_name
      )
    ),
    None,
  )

  if target is None:
    raise RuntimeError(
      f"function not found: {function_name}"
    )

  if target.end_lineno is None:
    raise RuntimeError(
      f"function has no end line: {function_name}"
    )

  lines = source.splitlines(
    keepends=True
  )

  return "".join(
    (
      *lines[
        :target.lineno - 1
      ],
      replacement.rstrip()
      + "\n\n",
      *lines[
        target.end_lineno:
      ],
    )
  )


def main() -> int:
  if not RENDERER.exists():
    raise RuntimeError(
      f"missing renderer: {RENDERER}"
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  shutil.copy2(
    RENDERER,
    BACKUP_DIR / RENDERER.name,
  )

  if TEST.exists():
    shutil.copy2(
      TEST,
      BACKUP_DIR / TEST.name,
    )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  updated = replace_function(
    source,
    "_phase159_r1_7b_normalize_public_exact_sequences",
    NEW_FUNCTION,
  )

  ast.parse(
    updated
  )

  RENDERER.write_text(
    updated,
    encoding="utf-8",
  )
  TEST.write_text(
    TEST_CONTENT,
    encoding="utf-8",
  )

  print(
    "Phase 159-R1-7b repair14 applied."
  )
  print(
    "Production: toda_group_proof_narrative_renderer.py"
  )
  print(
    "Changed function: "
    "_phase159_r1_7b_normalize_public_exact_sequences"
  )
  print(
    "New test: "
    "tests/test_phase159_r1_7b_repair14_map_property_anchor.py"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
