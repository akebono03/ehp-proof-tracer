from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
EXISTING_TEST = ROOT / "tests" / "test_phase157_r20_repair37_short_exact_after_map_support.py"
NEW_TEST = ROOT / "tests" / "test_phase159_r1_7b_exact_sequence_display_order.py"
BACKUP_DIR = ROOT / "phase159_r1_7b_backup_before_apply"

NEW_HELPERS = 'def _phase159_r1_7b_exactness_step_latex(\n  proof_step: ProofStep,\n) -> str | None:\n  if not isinstance(\n    proof_step.conclusion,\n    TodaProp42ExactnessStatement,\n  ):\n    return None\n\n  rendered = (\n    _render_generic_narrative_step(\n      proof_step\n    )\n  )\n\n  if (\n    not rendered.startswith(\n      "$"\n    )\n    or not rendered.endswith(\n      "$"\n    )\n  ):\n    return None\n\n  latex = rendered[\n    1:-1\n  ]\n  english_suffix = (\n    r" \\text{ is exact}"\n  )\n\n  if latex.endswith(\n    english_suffix\n  ):\n    latex = latex[\n      :-len(\n        english_suffix\n      )\n    ]\n\n  return latex\n\n\ndef _phase159_r1_7b_inline_exactness_latex(\n  line: str,\n) -> str | None:\n  stripped = line.strip()\n  suffix = "$ は完全である."\n\n  if (\n    not stripped.startswith(\n      "$"\n    )\n    or not stripped.endswith(\n      suffix\n    )\n  ):\n    return None\n\n  latex = stripped[\n    1:-len(\n      suffix\n    )\n  ]\n\n  if (\n    r"\\xrightarrow{" not in latex\n    and r"\\longrightarrow" not in latex\n  ):\n    return None\n\n  return latex\n\n\ndef _phase159_r1_7b_inline_short_exact_latex(\n  line: str,\n) -> str | None:\n  stripped = line.strip()\n\n  if not stripped.startswith(\n    r"$0\\longrightarrow "\n  ):\n    return None\n\n  if stripped.endswith(\n    "$."\n  ):\n    latex = stripped[\n      1:-2\n    ]\n  elif stripped.endswith(\n    "$"\n  ):\n    latex = stripped[\n      1:-1\n    ]\n  else:\n    return None\n\n  if not latex.endswith(\n    r"\\longrightarrow 0"\n  ):\n    return None\n\n  return latex\n\n\ndef _phase159_r1_7b_display_math_lines(\n  latex: str,\n) -> tuple[\n  str,\n  ...,\n]:\n  return (\n    r"\\[",\n    latex.rstrip(\n      "."\n    )\n    + ".",\n    r"\\]",\n    "",\n  )\n\n\ndef _phase159_r1_7b_map_property_signature(\n  line: str,\n) -> tuple[\n  str,\n  str,\n  str,\n] | None:\n  stripped = line.strip()\n\n  if not stripped.startswith(\n    "$"\n  ):\n    return None\n\n  math_end = stripped.find(\n    "$",\n    1,\n  )\n\n  if math_end < 0:\n    return None\n\n  suffix = stripped[\n    math_end + 1:\n  ].strip()\n\n  if not (\n    suffix.startswith(\n      "は単射"\n    )\n    or suffix.startswith(\n      "は全射"\n    )\n    or suffix.startswith(\n      "は零写像"\n    )\n    or suffix.startswith(\n      "は同型"\n    )\n  ):\n    return None\n\n  math = stripped[\n    1:math_end\n  ]\n\n  if ": " not in math:\n    return None\n\n  map_name, map_expression = math.split(\n    ": ",\n    1,\n  )\n\n  arrow = r" \\to "\n\n  if arrow not in map_expression:\n    return None\n\n  source, target = map_expression.split(\n    arrow,\n    1,\n  )\n\n  if (\n    not source.startswith(\n      r"\\pi_{"\n    )\n    or not target.startswith(\n      r"\\pi_{"\n    )\n  ):\n    return None\n\n  return (\n    map_name,\n    source,\n    target,\n  )\n\n\ndef _phase159_r1_7b_exactness_matches_map_property(\n  exactness_latex: str,\n  signature: tuple[\n    str,\n    str,\n    str,\n  ],\n) -> bool:\n  map_name, source, target = signature\n  map_segment = (\n    source\n    + r" \\xrightarrow{"\n    + map_name\n    + "} "\n    + target\n  )\n\n  return (\n    map_segment\n    in exactness_latex\n  )\n\n\ndef _phase159_r1_7b_find_display_math_span(\n  lines: list[\n    str\n  ],\n  latex: str,\n) -> tuple[\n  int,\n  int,\n] | None:\n  normalized_target = latex.rstrip(\n    "."\n  )\n  index = 0\n\n  while index < len(\n    lines\n  ):\n    if lines[\n      index\n    ].strip() != r"\\[":\n      index += 1\n      continue\n\n    end_index = index + 1\n    inner_lines = []\n\n    while (\n      end_index < len(\n        lines\n      )\n      and lines[\n        end_index\n      ].strip() != r"\\]"\n    ):\n      if lines[\n        end_index\n      ].strip():\n        inner_lines.append(\n          lines[\n            end_index\n          ].strip()\n        )\n      end_index += 1\n\n    if end_index >= len(\n      lines\n    ):\n      return None\n\n    normalized_inner = " ".join(\n      inner_lines\n    ).rstrip(\n      "."\n    )\n\n    if (\n      normalized_inner\n      == normalized_target\n    ):\n      span_end = end_index + 1\n\n      if (\n        span_end < len(\n          lines\n        )\n        and not lines[\n          span_end\n        ].strip()\n      ):\n        span_end += 1\n\n      return (\n        index,\n        span_end,\n      )\n\n    index = end_index + 1\n\n  return None\n\n\ndef _phase159_r1_7b_next_nonblank_index(\n  lines: list[\n    str\n  ],\n  start: int,\n) -> int | None:\n  return next(\n    (\n      index\n      for index in range(\n        start,\n        len(\n          lines\n        ),\n      )\n      if lines[\n        index\n      ].strip()\n    ),\n    None,\n  )\n\n\ndef _phase159_r1_7b_normalize_public_exact_sequences(\n  presentation: TodaGroupProofPresentation,\n  proof_body: list[\n    str\n  ],\n) -> list[\n  str\n]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    proof_body,\n    list,\n  ):\n    raise TypeError(\n      "proof_body must be a list"\n    )\n\n  exactness_latex = tuple(\n    latex\n    for latex in (\n      _phase159_r1_7b_exactness_step_latex(\n        node.proof_step\n      )\n      for node in presentation.nodes\n    )\n    if latex is not None\n  )\n\n  lines = []\n\n  for line in proof_body:\n    inline_exactness = (\n      _phase159_r1_7b_inline_exactness_latex(\n        line\n      )\n    )\n\n    if inline_exactness is not None:\n      lines.extend(\n        _phase159_r1_7b_display_math_lines(\n          inline_exactness\n        )\n      )\n      continue\n\n    inline_short_exact = (\n      _phase159_r1_7b_inline_short_exact_latex(\n        line\n      )\n    )\n\n    if inline_short_exact is not None:\n      lines.extend(\n        _phase159_r1_7b_display_math_lines(\n          inline_short_exact\n        )\n      )\n      continue\n\n    lines.append(\n      line\n    )\n\n  connector_index = 0\n\n  while connector_index < len(\n    lines\n  ):\n    if lines[\n      connector_index\n    ].strip() != "完全性より,":\n      connector_index += 1\n      continue\n\n    property_index = (\n      _phase159_r1_7b_next_nonblank_index(\n        lines,\n        connector_index + 1,\n      )\n    )\n\n    if property_index is None:\n      break\n\n    signature = (\n      _phase159_r1_7b_map_property_signature(\n        lines[\n          property_index\n        ]\n      )\n    )\n\n    if signature is None:\n      connector_index += 1\n      continue\n\n    matching_latex = next(\n      (\n        latex\n        for latex in exactness_latex\n        if (\n          _phase159_r1_7b_exactness_matches_map_property(\n            latex,\n            signature,\n          )\n        )\n      ),\n      None,\n    )\n\n    if matching_latex is None:\n      connector_index += 1\n      continue\n\n    existing_span = (\n      _phase159_r1_7b_find_display_math_span(\n        lines,\n        matching_latex,\n      )\n    )\n\n    if (\n      existing_span is not None\n      and existing_span[\n        0\n      ] < connector_index\n    ):\n      connector_index += 1\n      continue\n\n    if existing_span is not None:\n      span_start, span_end = existing_span\n      del lines[\n        span_start:span_end\n      ]\n\n      if span_start < connector_index:\n        connector_index -= (\n          span_end\n          - span_start\n        )\n\n    display_lines = list(\n      _phase159_r1_7b_display_math_lines(\n        matching_latex\n      )\n    )\n    lines[\n      connector_index:connector_index\n    ] = display_lines\n\n    connector_index += len(\n      display_lines\n    ) + 1\n\n  return lines\n\n\n'
NEW_TEST_CONTENT = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase159_r1_7b_render(\n  n: int,\n  k: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[\n      0\n    ].source_candidate.group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_7b_pi6_3_short_exact_sequence_is_display_math():\n  rendered = _phase159_r1_7b_render(\n    3,\n    3,\n  )\n  short_exact = (\n    "\\\\[\\n"\n    r"0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    "\\\\longrightarrow 0.\\n"\n    "\\\\]"\n  )\n\n  assert short_exact in rendered\n  assert (\n    r"$0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    r"\\longrightarrow 0$"\n    not in rendered\n  )\n\n\ndef test_phase159_r1_7b_pi11_4_delta_surjectivity_has_matching_exactness_before_it():\n  rendered = _phase159_r1_7b_render(\n    4,\n    7,\n  )\n  matching_exactness = (\n    "\\\\[\\n"\n    r"\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} "\n    r"\\xrightarrow{\\Delta} \\pi_{8}^{2}."\n    "\\n\\\\]"\n  )\n  surjectivity_reason = (\n    "完全性より,"\n  )\n  surjectivity = (\n    r"$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$"\n    " は全射."\n  )\n\n  assert matching_exactness in rendered\n  assert surjectivity_reason in rendered\n  assert surjectivity in rendered\n  assert rendered.index(\n    matching_exactness\n  ) < rendered.index(\n    surjectivity_reason\n  )\n  assert rendered.index(\n    surjectivity_reason\n  ) < rendered.index(\n    surjectivity\n  )\n\n\ndef test_phase159_r1_7b_pi11_4_visible_exactness_windows_use_display_math():\n  rendered = _phase159_r1_7b_render(\n    4,\n    7,\n  )\n  second_exactness = (\n    "\\\\[\\n"\n    r"\\pi_{9}^{2} \\xrightarrow{E} \\pi_{10}^{3} "\n    r"\\xrightarrow{H} \\pi_{10}^{5}."\n    "\\n\\\\]"\n  )\n\n  assert second_exactness in rendered\n  assert (\n    r"$\\pi_{9}^{2} \\xrightarrow{E} \\pi_{10}^{3} "\n    r"\\xrightarrow{H} \\pi_{10}^{5}$ は完全である."\n    not in rendered\n  )\n'
UPDATED_EXISTING_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _body_pi6_3_repair37() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate.group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  return rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n\ndef test_phase157_r20_repair37_short_exact_follows_surjectivity():\n  body = _body_pi6_3_repair37()\n\n  surjectivity = (\n    r"$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ "\n    "は全射である."\n  )\n  reason = (\n    "この完全性と, 左の写像が単射, "\n    "右の写像が全射であることより, "\n    "次の短完全列を得る."\n  )\n  short_exact = (\n    "\\\\[\\n"\n    r"0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    "\\\\longrightarrow 0.\\n"\n    "\\\\]"\n  )\n\n  assert surjectivity in body\n  assert reason in body\n  assert short_exact in body\n\n  assert body.index(\n    surjectivity\n  ) < body.index(\n    reason\n  )\n  assert body.index(\n    reason\n  ) < body.index(\n    short_exact\n  )\n\n\ndef test_phase157_r20_repair37_short_exact_follows_injectivity():\n  body = _body_pi6_3_repair37()\n\n  injectivity = (\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "\n    "は単射である."\n  )\n  short_exact = (\n    "\\\\[\\n"\n    r"0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    "\\\\longrightarrow 0.\\n"\n    "\\\\]"\n  )\n\n  assert body.index(\n    injectivity\n  ) < body.index(\n    short_exact\n  )\n'

OLD_CALL = """  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )

  lines = [
"""

NEW_CALL = """  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )
  proof_body = (
    _phase159_r1_7b_normalize_public_exact_sequences(
      presentation,
      proof_body,
    )
  )

  lines = [
"""


def main() -> int:
  if not RENDERER.exists():
    raise RuntimeError(f"missing production file: {RENDERER}")
  if not EXISTING_TEST.exists():
    raise RuntimeError(f"missing existing test: {EXISTING_TEST}")

  BACKUP_DIR.mkdir(parents=True, exist_ok=True)
  shutil.copy2(RENDERER, BACKUP_DIR / RENDERER.name)
  shutil.copy2(EXISTING_TEST, BACKUP_DIR / EXISTING_TEST.name)

  source = RENDERER.read_text(encoding="utf-8-sig")
  marker = "def _phase158_normalize_public_narrative_contract(\n"

  if NEW_HELPERS.strip() not in source:
    if marker not in source:
      raise RuntimeError("public narrative normalizer anchor not found")
    source = source.replace(marker, NEW_HELPERS + marker, 1)

  if NEW_CALL not in source:
    if OLD_CALL not in source:
      raise RuntimeError("proof-body normalization call anchor not found")
    source = source.replace(OLD_CALL, NEW_CALL, 1)

  RENDERER.write_text(source, encoding="utf-8")
  EXISTING_TEST.write_text(UPDATED_EXISTING_TEST, encoding="utf-8")
  NEW_TEST.write_text(NEW_TEST_CONTENT, encoding="utf-8")

  print("Phase 159-R1-7b applied.")
  print("Production: toda_group_proof_narrative_renderer.py")
  print("Updated test: tests/test_phase157_r20_repair37_short_exact_after_map_support.py")
  print("New test: tests/test_phase159_r1_7b_exact_sequence_display_order.py")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
