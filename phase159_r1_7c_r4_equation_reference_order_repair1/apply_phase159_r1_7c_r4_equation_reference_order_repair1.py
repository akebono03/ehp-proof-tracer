from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

PRODUCTION = (
  ROOT
  / "toda_group_proof_narrative_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_7c_r4_equation_reference_order_repair1.py"
)

HELPER = 'def _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  proof_marker = "## 証明\\n\\n"\n  marker_index = rendered.find(\n    proof_marker\n  )\n\n  if marker_index < 0:\n    return rendered\n\n  proof_start = (\n    marker_index\n    + len(\n      proof_marker\n    )\n  )\n  prefix = rendered[\n    :proof_start\n  ]\n  proof_body = rendered[\n    proof_start:\n  ]\n\n  had_trailing_newline = (\n    rendered.endswith(\n      "\\n"\n    )\n  )\n  paragraphs = proof_body.rstrip(\n    "\\n"\n  ).split(\n    "\\n\\n"\n  )\n\n  tag_pattern = re.compile(\n    r"\\\\tag\\{(\\d+)\\}"\n  )\n  reference_pattern = re.compile(\n    (\n      r"^"\n      r"((?:\\(\\d+\\)"\n      r"(?:,\\s*|\\s+と\\s+)?)+)"\n      r"\\s*より,"\n    )\n  )\n  parenthesized_number_pattern = re.compile(\n    r"\\((\\d+)\\)"\n  )\n\n  changed = True\n\n  while changed:\n    changed = False\n    tag_paragraph_by_number = {}\n\n    for paragraph_index, paragraph in enumerate(\n      paragraphs\n    ):\n      for match in tag_pattern.finditer(\n        paragraph\n      ):\n        number = int(\n          match.group(\n            1\n          )\n        )\n        tag_paragraph_by_number.setdefault(\n          number,\n          paragraph_index,\n        )\n\n    for conclusion_index, paragraph in enumerate(\n      paragraphs\n    ):\n      stripped = paragraph.strip()\n      reference_match = reference_pattern.match(\n        stripped\n      )\n\n      if reference_match is None:\n        continue\n\n      reference_numbers = tuple(\n        int(\n          number\n        )\n        for number in parenthesized_number_pattern.findall(\n          reference_match.group(\n            1\n          )\n        )\n      )\n\n      if not reference_numbers:\n        continue\n\n      referenced_indices = tuple(\n        tag_paragraph_by_number.get(\n          number\n        )\n        for number in reference_numbers\n      )\n\n      if any(\n        index is None\n        for index in referenced_indices\n      ):\n        continue\n\n      target_index = max(\n        index\n        for index in referenced_indices\n        if index is not None\n      )\n\n      if target_index < conclusion_index:\n        continue\n\n      conclusion = paragraphs.pop(\n        conclusion_index\n      )\n\n      if conclusion_index < target_index:\n        target_index -= 1\n\n      paragraphs.insert(\n        target_index + 1,\n        conclusion,\n      )\n      changed = True\n      break\n\n  result = (\n    prefix\n    + "\\n\\n".join(\n      paragraphs\n    )\n  )\n\n  if had_trailing_newline:\n    result += "\\n"\n\n  return result\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n      rendered\n    )\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions,\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _public_narrative(\n  n: int,\n  k: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_7c_r4_pi5_3_places_isomorphism_after_both_numbered_premises():\n  rendered = _public_narrative(\n    3,\n    2,\n  )\n\n  injective = (\n    r"$E: \\pi_{4}^{2} \\to \\pi_{5}^{3}\\tag{1}$ は単射."\n  )\n  surjective = (\n    r"これより, $E: \\pi_{4}^{2} \\to \\pi_{5}^{3}\\tag{2}$ は全射."\n  )\n  isomorphism = (\n    r"(1), (2) より, $E: \\pi_{4}^{2} \\to \\pi_{5}^{3}$ は同型."\n  )\n\n  assert injective in rendered\n  assert surjective in rendered\n  assert isomorphism in rendered\n  assert (\n    rendered.index(\n      injective\n    )\n    < rendered.index(\n      surjective\n    )\n    < rendered.index(\n      isomorphism\n    )\n  )\n\n\ndef test_phase159_r1_7c_r4_pi3_2_keeps_valid_backward_equation_references():\n  rendered = _public_narrative(\n    2,\n    1,\n  )\n\n  injective = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}\\tag{1}$ は単射."\n  )\n  surjective = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}\\tag{2}$ は全射."\n  )\n  isomorphism = (\n    r"(1), (2) より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."\n  )\n\n  assert (\n    rendered.index(\n      injective\n    )\n    < rendered.index(\n      surjective\n    )\n    < rendered.index(\n      isomorphism\n    )\n  )\n\n\ndef test_phase159_r1_7c_r4_reorder_helper_moves_only_forward_reference_conclusion():\n  rendered = (\n    "# Group proof narrative\\n\\n"\n    "## 証明\\n\\n"\n    "(1), (2) より, $F: A \\\\to B$ は同型.\\n\\n"\n    "$F: A \\\\to B\\\\tag{1}$ は単射.\\n\\n"\n    "$F: A \\\\to B\\\\tag{2}$ は全射.\\n\\n"\n    "□\\n"\n  )\n\n  normalized = (\n    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n      rendered\n    )\n  )\n\n  injective = (\n    r"$F: A \\to B\\tag{1}$ は単射."\n  )\n  surjective = (\n    r"$F: A \\to B\\tag{2}$ は全射."\n  )\n  isomorphism = (\n    r"(1), (2) より, $F: A \\to B$ は同型."\n  )\n\n  assert (\n    normalized.index(\n      injective\n    )\n    < normalized.index(\n      surjective\n    )\n    < normalized.index(\n      isomorphism\n    )\n  )\n\n\ndef test_phase159_r1_7c_r4_reorder_helper_leaves_missing_reference_untouched():\n  rendered = (\n    "# Group proof narrative\\n\\n"\n    "## 証明\\n\\n"\n    "(1), (2) より, $F: A \\\\to B$ は同型.\\n\\n"\n    "$F: A \\\\to B\\\\tag{1}$ は単射.\\n\\n"\n    "□\\n"\n  )\n\n  normalized = (\n    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n      rendered\n    )\n  )\n\n  assert normalized == rendered\n'


def replace_function(
  source: str,
  function_name: str,
  new_source: str,
) -> str:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise SystemExit(
      f"function not found: {function_name}"
    )

  next_start = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_start < 0:
    end = len(
      source
    )
  else:
    end = next_start + 1

  return (
    source[:start]
    + new_source.rstrip()
    + "\n\n"
    + source[end:]
  )


def main() -> None:
  BACKUP.mkdir(
    parents=True,
    exist_ok=True,
  )

  shutil.copy2(
    PRODUCTION,
    BACKUP / PRODUCTION.name,
  )

  source = PRODUCTION.read_text(
    encoding="utf-8"
  )

  prerequisite = (
    "def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning("
  )

  if prerequisite not in source:
    raise SystemExit(
      "numbered-reasoning repair1 prerequisite helper not found"
    )

  helper_marker = (
    "def _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions("
  )

  if helper_marker not in source:
    render_marker = (
      "def render_toda_group_proof_narrative_markdown("
    )
    render_index = source.find(
      render_marker
    )

    if render_index < 0:
      raise SystemExit(
        "public narrative render function anchor not found"
      )

    source = (
      source[:render_index]
      + HELPER.rstrip()
      + "\n\n"
      + source[render_index:]
    )

  source = replace_function(
    source,
    "render_toda_group_proof_narrative_markdown",
    RENDER_FUNCTION,
  )

  PRODUCTION.write_text(
    source,
    encoding="utf-8",
  )

  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R4 equation-reference order repair1 applied."
  )
  print(
    "No semantic inference rules were added or changed."
  )
  print(
    "Only forward public equation-reference conclusion paragraphs are reordered."
  )


if __name__ == "__main__":
  main()
