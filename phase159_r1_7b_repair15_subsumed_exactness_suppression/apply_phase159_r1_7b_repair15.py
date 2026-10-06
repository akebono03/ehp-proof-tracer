from __future__ import annotations

import ast
from pathlib import Path
import shutil


ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_7b_repair15_subsumed_exactness.py"
BACKUP_DIR = ROOT / "phase159_r1_7b_repair15_backup_before_apply"

NEW_FUNCTION = 'def _phase159_r1_7b_normalize_public_exact_sequences(\n  presentation: TodaGroupProofPresentation,\n  proof_body: list[\n    str\n  ],\n) -> list[\n  str\n]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    proof_body,\n    list,\n  ):\n    raise TypeError(\n      "proof_body must be a list"\n    )\n\n  semantic_presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  exactness_latex = tuple(\n    latex\n    for latex in (\n      _phase159_r1_7b_exactness_step_latex(\n        node.proof_step\n      )\n      for node in semantic_presentation.nodes\n    )\n    if latex is not None\n  )\n\n  def canonical_exactness(\n    latex: str,\n  ) -> str:\n    return (\n      latex\n      .replace(\n        r"\\xrightarrow{Δ}",\n        r"\\xrightarrow{\\Delta}",\n      )\n      .strip()\n      .removesuffix(\n        "."\n      )\n      .strip()\n    )\n\n  canonical_exactness_latex = tuple(\n    canonical_exactness(\n      latex\n    )\n    for latex in exactness_latex\n  )\n\n  def canonical_typed_exactness(\n    latex: str,\n  ) -> str:\n    canonical = canonical_exactness(\n      latex\n    )\n\n    for (\n      typed_latex,\n      typed_canonical,\n    ) in zip(\n      exactness_latex,\n      canonical_exactness_latex,\n    ):\n      if canonical == typed_canonical:\n        return typed_latex\n\n    return canonical\n\n  def prior_display_covers(\n    lines: list[\n      str\n    ],\n    latex: str,\n    before_index: int,\n  ) -> bool:\n    target = canonical_exactness(\n      latex\n    )\n    index = 0\n\n    while index < min(\n      before_index,\n      len(\n        lines\n      ),\n    ):\n      if (\n        lines[\n          index\n        ].strip()\n        == r"\\["\n        and index + 2\n        < len(\n          lines\n        )\n        and lines[\n          index + 2\n        ].strip()\n        == r"\\]"\n      ):\n        displayed = (\n          canonical_exactness(\n            lines[\n              index + 1\n            ]\n          )\n        )\n\n        if target in displayed:\n          return True\n\n        index += 3\n        continue\n\n      index += 1\n\n    return False\n\n  lines = []\n\n  for line in proof_body:\n    inline_exactness = (\n      _phase159_r1_7b_inline_exactness_latex(\n        line\n      )\n    )\n\n    if inline_exactness is not None:\n      lines.extend(\n        _phase159_r1_7b_display_math_lines(\n          canonical_typed_exactness(\n            inline_exactness\n          )\n        )\n      )\n      continue\n\n    inline_short_exact = (\n      _phase159_r1_7b_inline_short_exact_latex(\n        line\n      )\n    )\n\n    if inline_short_exact is not None:\n      lines.extend(\n        _phase159_r1_7b_display_math_lines(\n          inline_short_exact\n        )\n      )\n      continue\n\n    lines.append(\n      line\n    )\n\n  line_index = 0\n\n  while line_index < len(\n    lines\n  ):\n    signature = (\n      _phase159_r1_7b_map_property_signature(\n        lines[\n          line_index\n        ]\n      )\n    )\n\n    if signature is None:\n      line_index += 1\n      continue\n\n    matching_latex = next(\n      (\n        latex\n        for latex in exactness_latex\n        if (\n          _phase159_r1_7b_exactness_matches_map_property(\n            latex,\n            signature,\n          )\n        )\n      ),\n      None,\n    )\n\n    if matching_latex is None:\n      line_index += 1\n      continue\n\n    if prior_display_covers(\n      lines,\n      matching_latex,\n      line_index,\n    ):\n      line_index += 1\n      continue\n\n    existing_span = (\n      _phase159_r1_7b_find_display_math_span(\n        lines,\n        matching_latex,\n      )\n    )\n\n    if (\n      existing_span is not None\n      and existing_span[\n        0\n      ] < line_index\n    ):\n      line_index += 1\n      continue\n\n    if existing_span is not None:\n      span_start, span_end = existing_span\n\n      del lines[\n        span_start:span_end\n      ]\n\n      if span_start < line_index:\n        line_index -= (\n          span_end\n          - span_start\n        )\n\n    display_lines = list(\n      _phase159_r1_7b_display_math_lines(\n        matching_latex\n      )\n    )\n\n    lines[\n      line_index:line_index\n    ] = display_lines\n\n    line_index += (\n      len(\n        display_lines\n      )\n      + 1\n    )\n\n  result = []\n  displayed_exactness = []\n  line_index = 0\n\n  while line_index < len(\n    lines\n  ):\n    if (\n      lines[\n        line_index\n      ].strip()\n      == r"\\["\n      and line_index + 2\n      < len(\n        lines\n      )\n      and lines[\n        line_index + 2\n      ].strip()\n      == r"\\]"\n    ):\n      content = canonical_exactness(\n        lines[\n          line_index + 1\n        ]\n      )\n\n      is_typed_exactness = (\n        content\n        in canonical_exactness_latex\n      )\n\n      if (\n        is_typed_exactness\n        and any(\n          content in earlier\n          for earlier in displayed_exactness\n        )\n      ):\n        line_index += 3\n        continue\n\n      displayed_exactness.append(\n        content\n      )\n\n      result.extend(\n        lines[\n          line_index:line_index + 3\n        ]\n      )\n      line_index += 3\n      continue\n\n    result.append(\n      lines[\n        line_index\n      ]\n    )\n    line_index += 1\n\n  return result\n'
TEST_CONTENT = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render(\n  n: int,\n  k: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_7b_repair15_pi6_3_subsumed_windows_are_not_repeated():\n  rendered = _render(\n    3,\n    3,\n  )\n\n  h_delta = (\n    "\\\\[\\n"\n    r"\\pi_{7}^{3} \\xrightarrow{H} \\pi_{7}^{5} "\n    r"\\xrightarrow{\\Delta} \\pi_{5}^{2}."\n    "\\n\\\\]"\n  )\n  delta_e = (\n    "\\\\[\\n"\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} \\pi_{5}^{2} "\n    r"\\xrightarrow{E} \\pi_{6}^{3}."\n    "\\n\\\\]"\n  )\n\n  assert h_delta not in rendered\n  assert delta_e not in rendered\n\n  assert (\n    "\\\\[\\n"\n    r"\\pi_{7}^{3} \\xrightarrow{H} \\pi_{7}^{5} "\n    r"\\xrightarrow{\\Delta} \\pi_{5}^{2} "\n    r"\\xrightarrow{E} \\pi_{6}^{3}."\n    "\\n\\\\]"\n    in rendered\n  )\n\n\ndef test_phase159_r1_7b_repair15_pi6_3_exactness_uses_canonical_delta():\n  rendered = _render(\n    3,\n    3,\n  )\n\n  assert r"\\xrightarrow{Δ}" not in rendered\n\n\ndef test_phase159_r1_7b_repair15_pi11_4_keeps_distinct_exactness_windows():\n  rendered = _render(\n    4,\n    7,\n  )\n\n  h_delta = (\n    "\\\\[\\n"\n    r"\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} "\n    r"\\xrightarrow{\\Delta} \\pi_{8}^{2}."\n    "\\n\\\\]"\n  )\n  e_h = (\n    "\\\\[\\n"\n    r"\\pi_{9}^{2} \\xrightarrow{E} \\pi_{10}^{3} "\n    r"\\xrightarrow{H} \\pi_{10}^{5}."\n    "\\n\\\\]"\n  )\n\n  assert rendered.count(\n    h_delta\n  ) == 1\n  assert rendered.count(\n    e_h\n  ) == 1\n'


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
    "Phase 159-R1-7b repair15 applied."
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
    "tests/test_phase159_r1_7b_repair15_subsumed_exactness.py"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
