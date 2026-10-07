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
  / "test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py"
)

HELPER = 'def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  proof_marker = "## 証明\\n\\n"\n  marker_index = rendered.find(\n    proof_marker\n  )\n\n  if marker_index < 0:\n    return rendered\n\n  proof_start = (\n    marker_index\n    + len(\n      proof_marker\n    )\n  )\n  prefix = rendered[\n    :proof_start\n  ]\n  proof_body = rendered[\n    proof_start:\n  ]\n  lines = proof_body.splitlines()\n\n  reference_prefix = re.compile(\n    r"^\\[R\\d+\\]より,\\s*"\n  )\n  connector_prefix = re.compile(\n    r"^\\((\\d+)\\),\\s*\\((\\d+)\\)\\s+より,\\s*"\n  )\n  tag_pattern = re.compile(\n    r"\\\\tag\\{(\\d+)\\}"\n  )\n\n  def map_property(\n    line: str,\n    suffix: str,\n  ) -> tuple[\n    str,\n    int | None,\n  ] | None:\n    stripped = line.strip()\n    stripped = reference_prefix.sub(\n      "",\n      stripped,\n    )\n\n    if not stripped.endswith(\n      suffix\n    ):\n      return None\n\n    map_text = stripped[\n      :-len(\n        suffix\n      )\n    ].strip()\n\n    tag_match = tag_pattern.search(\n      map_text\n    )\n    tag_number = (\n      int(\n        tag_match.group(\n          1\n        )\n      )\n      if tag_match is not None\n      else None\n    )\n    map_text = tag_pattern.sub(\n      "",\n      map_text,\n    ).strip()\n\n    return (\n      map_text,\n      tag_number,\n    )\n\n  def isomorphism_map(\n    line: str,\n  ) -> tuple[\n    str,\n    bool,\n  ] | None:\n    stripped = line.strip()\n\n    if reference_prefix.match(\n      stripped\n    ):\n      return None\n\n    had_connector = (\n      connector_prefix.match(\n        stripped\n      )\n      is not None\n    )\n    stripped = connector_prefix.sub(\n      "",\n      stripped,\n    )\n\n    for suffix in (\n      " は同型.",\n      " は同型写像.",\n      " は同型である.",\n      " は同型写像である.",\n    ):\n      if stripped.endswith(\n        suffix\n      ):\n        return (\n          tag_pattern.sub(\n            "",\n            stripped[\n              :-len(\n                suffix\n              )\n            ].strip(),\n          ),\n          had_connector,\n        )\n\n    return None\n\n  injective_by_map = {}\n  surjective_by_map = {}\n  isomorphism_by_map = {}\n\n  for index, line in enumerate(\n    lines\n  ):\n    injective = map_property(\n      line,\n      " は単射.",\n    )\n\n    if injective is not None:\n      injective_by_map.setdefault(\n        injective[0],\n        []\n      ).append(\n        (\n          index,\n          injective[1],\n        )\n      )\n\n    surjective = map_property(\n      line,\n      " は全射.",\n    )\n\n    if surjective is not None:\n      surjective_by_map.setdefault(\n        surjective[0],\n        []\n      ).append(\n        (\n          index,\n          surjective[1],\n        )\n      )\n\n    isomorphism = isomorphism_map(\n      line\n    )\n\n    if isomorphism is not None:\n      isomorphism_by_map.setdefault(\n        isomorphism[0],\n        []\n      ).append(\n        (\n          index,\n          isomorphism[1],\n        )\n      )\n\n  existing_numbers = tuple(\n    int(\n      match.group(\n        1\n      )\n    )\n    for line in lines\n    for match in tag_pattern.finditer(\n      line\n    )\n  )\n  next_number = (\n    max(\n      existing_numbers,\n      default=0,\n    )\n    + 1\n  )\n\n  def ensure_tag(\n    line_index: int,\n    number: int,\n  ) -> None:\n    line = lines[\n      line_index\n    ]\n\n    if tag_pattern.search(\n      line\n    ):\n      return\n\n    suffix_index = max(\n      line.rfind(\n        " は単射."\n      ),\n      line.rfind(\n        " は全射."\n      ),\n    )\n\n    if suffix_index < 0:\n      return\n\n    closing = line.rfind(\n      "$",\n      0,\n      suffix_index,\n    )\n\n    if closing < 0:\n      return\n\n    lines[\n      line_index\n    ] = (\n      line[\n        :closing\n      ]\n      + r"\\tag{"\n      + str(\n        number\n      )\n      + "}"\n      + line[\n        closing:\n      ]\n    )\n\n  for map_text in tuple(\n    isomorphism_by_map\n  ):\n    injective_rows = injective_by_map.get(\n      map_text,\n      ()\n    )\n    surjective_rows = surjective_by_map.get(\n      map_text,\n      ()\n    )\n\n    if (\n      not injective_rows\n      or not surjective_rows\n    ):\n      continue\n\n    injective_index, injective_number = (\n      injective_rows[\n        0\n      ]\n    )\n    surjective_index, surjective_number = (\n      surjective_rows[\n        0\n      ]\n    )\n\n    if injective_number is None:\n      injective_number = next_number\n      next_number += 1\n      ensure_tag(\n        injective_index,\n        injective_number,\n      )\n\n    if surjective_number is None:\n      surjective_number = next_number\n      next_number += 1\n      ensure_tag(\n        surjective_index,\n        surjective_number,\n      )\n\n    isomorphism_index, _had_connector = (\n      isomorphism_by_map[\n        map_text\n      ][\n        0\n      ]\n    )\n    lines[\n      isomorphism_index\n    ] = (\n      "("\n      + str(\n        injective_number\n      )\n      + "), ("\n      + str(\n        surjective_number\n      )\n      + ") より, "\n      + map_text\n      + " は同型."\n    )\n\n  return (\n    prefix\n    + "\\n".join(\n      lines\n    )\n    + (\n      "\\n"\n      if rendered.endswith(\n        "\\n"\n      )\n      else ""\n    )\n  )\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _public_narrative(\n  n: int,\n  k: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_7c_r4_pi11_6_numbers_existing_hopf_reasoning():\n  rendered = _public_narrative(\n    6,\n    5,\n  )\n\n  assert (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}\\tag{1}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}\\tag{2}$ は全射."\n    in rendered\n  )\n  assert (\n    r"(1), (2) より, $H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は同型."\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は同型写像である."\n    not in rendered\n  )\n\n\ndef test_phase159_r1_7c_r4_pi3_2_keeps_existing_numbered_hopf_reasoning():\n  rendered = _public_narrative(\n    2,\n    1,\n  )\n\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}\\tag{1}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}\\tag{2}$ は全射."\n    in rendered\n  )\n  assert (\n    r"(1), (2) より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."\n    in rendered\n  )\n\n\ndef test_phase159_r1_7c_r4_delta_pairs_without_isomorphism_are_not_numbered():\n  for n, k, map_text in (\n    (\n      3,\n      6,\n      r"\\Delta: \\pi_{9}^{5} \\to \\pi_{7}^{2}",\n    ),\n    (\n      3,\n      7,\n      r"\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}",\n    ),\n  ):\n    rendered = _public_narrative(\n      n,\n      k,\n    )\n\n    assert (\n      "$"\n      + map_text\n      + "$ は単射."\n      in rendered\n    )\n    assert (\n      "$"\n      + map_text\n      + "$ は全射."\n      in rendered\n    )\n    assert (\n      "$"\n      + map_text\n      + r"\\tag{"\n      not in rendered\n    )\n    assert (\n      "$"\n      + map_text\n      + "$ は同型."\n      not in rendered\n    )\n    assert (\n      "$"\n      + map_text\n      + "$ は同型写像である."\n      not in rendered\n    )\n\n\ndef test_phase159_r1_7c_r4_numbered_reasoning_is_general_not_pi11_hardcoded():\n  from toda_group_proof_narrative_renderer import (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,\n  )\n\n  rendered = (\n    "# Group proof narrative\\n\\n"\n    "## 証明対象\\n\\n"\n    "target\\n\\n"\n    "## 使用する結果\\n\\n"\n    "---\\n\\n"\n    "## 証明\\n\\n"\n    "$F: A \\\\to B$ は単射.\\n"\n    "$F: A \\\\to B$ は全射.\\n"\n    "$F: A \\\\to B$ は同型写像である.\\n\\n"\n    "□\\n"\n  )\n\n  normalized = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n\n  assert (\n    r"$F: A \\to B\\tag{1}$ は単射."\n    in normalized\n  )\n  assert (\n    r"$F: A \\to B\\tag{2}$ は全射."\n    in normalized\n  )\n  assert (\n    r"(1), (2) より, $F: A \\to B$ は同型."\n    in normalized\n  )\n'


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

  required_helper = (
    "def _phase159_r1_7c_r4_normalize_public_map_property_prose("
  )

  if required_helper not in source:
    raise SystemExit(
      "repair1 prerequisite helper not found; "
      "apply map-property dearu repair1 first"
    )

  helper_marker = (
    "def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning("
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
    "Phase 159 R1-7c R4 numbered map-property reasoning repair1 applied."
  )
  print(
    "No semantic inference rules were added or changed."
  )
  print(
    "Only existing public injective + surjective + isomorphism trios are normalized."
  )


if __name__ == "__main__":
  main()
