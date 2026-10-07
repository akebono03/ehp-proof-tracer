from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
RENDERER_PATH = REPO_ROOT / "toda_group_proof_narrative_renderer.py"
PI3_TEST_PATH = REPO_ROOT / "tests" / "test_phase159_r1_2_pi3_2_narrative_repair.py"
NUMBERED_TEST_PATH = REPO_ROOT / "tests" / "test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py"
REPAIR25_TEST_PATH = REPO_ROOT / "tests" / "test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py"
REPAIR24_TEST_PATH = REPO_ROOT / "tests" / "test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair24.py"
BACKUP_DIR = Path(__file__).resolve().parent / "backup_before_apply"

NEW_RECURSIVE_HELPER = 'def _phase159_recursive_map_property_triples(\n  presentation: TodaGroupProofPresentation,\n) -> tuple[\n  tuple[\n    ProofStep,\n    ProofStep,\n    ProofStep,\n  ],\n  ...,\n]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  steps = (\n    _phase159_r1_6c_recursive_proof_steps(\n      presentation.root_step\n    )\n  )\n  injective_by_map = {}\n  surjective_by_map = {}\n  isomorphism_steps = []\n\n  for proof_step in steps:\n    statement = proof_step.conclusion\n    group_map = getattr(\n      statement,\n      "map",\n      None,\n    )\n\n    if group_map is None:\n      continue\n\n    if isinstance(\n      statement,\n      _GENERIC_INJECTIVE_STATEMENT_TYPES,\n    ):\n      injective_by_map.setdefault(\n        group_map,\n        proof_step,\n      )\n      continue\n\n    if isinstance(\n      statement,\n      _GENERIC_SURJECTIVE_STATEMENT_TYPES,\n    ):\n      surjective_by_map.setdefault(\n        group_map,\n        proof_step,\n      )\n      continue\n\n    if isinstance(\n      statement,\n      _GENERIC_ISOMORPHISM_STATEMENT_TYPES,\n    ):\n      isomorphism_steps.append(\n        proof_step\n      )\n\n  triples = []\n\n  for isomorphism_step in isomorphism_steps:\n    group_map = getattr(\n      isomorphism_step.conclusion,\n      "map",\n      None,\n    )\n\n    if group_map is None:\n      continue\n\n    injective_step = (\n      injective_by_map.get(\n        group_map\n      )\n    )\n    surjective_step = (\n      surjective_by_map.get(\n        group_map\n      )\n    )\n\n    if (\n      injective_step is None\n      or surjective_step is None\n    ):\n      continue\n\n    triples.append(\n      (\n        injective_step,\n        surjective_step,\n        isomorphism_step,\n      )\n    )\n\n  return tuple(\n    triples\n  )\n'
NEW_NUMBERED = 'def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n  rendered: str,\n  presentation: TodaGroupProofPresentation | None = None,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  if (\n    presentation is not None\n    and not isinstance(\n      presentation,\n      TodaGroupProofPresentation,\n    )\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation or None"\n    )\n\n  if presentation is None:\n    return rendered\n\n  proof_marker = "## 証明\\n\\n"\n  marker_index = rendered.find(\n    proof_marker\n  )\n\n  if marker_index < 0:\n    return rendered\n\n  proof_start = (\n    marker_index\n    + len(\n      proof_marker\n    )\n  )\n  prefix = rendered[\n    :proof_start\n  ]\n  proof_body = rendered[\n    proof_start:\n  ]\n  lines = proof_body.splitlines()\n\n  (\n    semantic_presentation,\n    semantic_sidecar,\n    _primary_component,\n  ) = _phase159_public_semantic_projection_context(\n    presentation\n  )\n\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      semantic_presentation,\n      semantic_sidecar,\n    )\n  )\n  exactness_conclusion_step_ids = {\n    id(\n      reason.conclusion_step\n    )\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n    )\n  }\n\n  tag_pattern = re.compile(\n    r"\\\\tag\\{(\\d+)\\}"\n  )\n\n  existing_numbers = tuple(\n    int(\n      match.group(\n        1\n      )\n    )\n    for line in lines\n    for match in tag_pattern.finditer(\n      line\n    )\n  )\n  next_number = (\n    max(\n      existing_numbers,\n      default=0,\n    )\n    + 1\n  )\n\n  def semantic_map_latex(\n    proof_step: ProofStep,\n  ) -> str | None:\n    group_map = getattr(\n      proof_step.conclusion,\n      "map",\n      None,\n    )\n\n    if group_map is None:\n      return None\n\n    return (\n      _render_generic_narrative_group_map_latex(\n        group_map\n      )\n    )\n\n  def find_property_line(\n    proof_step: ProofStep,\n    property_label: str,\n  ) -> tuple[\n    int,\n    int | None,\n  ] | None:\n    map_latex = semantic_map_latex(\n      proof_step\n    )\n\n    if map_latex is None:\n      return None\n\n    prose_marker = (\n      "は"\n      + property_label\n    )\n    display_marker = (\n      r"\\text{は"\n      + property_label\n      + "}"\n    )\n\n    matches = []\n\n    for index, line in enumerate(\n      lines\n    ):\n      if map_latex not in line:\n        continue\n\n      if (\n        prose_marker not in line\n        and display_marker not in line\n      ):\n        continue\n\n      tag_match = tag_pattern.search(\n        line\n      )\n      matches.append(\n        (\n          index,\n          (\n            int(\n              tag_match.group(\n                1\n              )\n            )\n            if tag_match is not None\n            else None\n          ),\n        )\n      )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  def find_isomorphism_line(\n    proof_step: ProofStep,\n  ) -> int | None:\n    map_latex = semantic_map_latex(\n      proof_step\n    )\n\n    if map_latex is None:\n      return None\n\n    matches = [\n      index\n      for index, line in enumerate(\n        lines\n      )\n      if (\n        map_latex in line\n        and (\n          "は同型." in line\n          or "は同型写像." in line\n          or "は同型である." in line\n          or "は同型写像である." in line\n        )\n      )\n    ]\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  numbered_by_index = {}\n  isomorphism_by_index = {}\n\n  for (\n    injective_step,\n    surjective_step,\n    isomorphism_step,\n  ) in _phase159_recursive_map_property_triples(\n    presentation\n  ):\n    injective_row = find_property_line(\n      injective_step,\n      "単射",\n    )\n    surjective_row = find_property_line(\n      surjective_step,\n      "全射",\n    )\n    isomorphism_index = (\n      find_isomorphism_line(\n        isomorphism_step\n      )\n    )\n\n    if (\n      injective_row is None\n      or surjective_row is None\n      or isomorphism_index is None\n    ):\n      continue\n\n    (\n      injective_index,\n      injective_number,\n    ) = injective_row\n    (\n      surjective_index,\n      surjective_number,\n    ) = surjective_row\n\n    if injective_number is None:\n      injective_number = next_number\n      next_number += 1\n\n    if surjective_number is None:\n      surjective_number = next_number\n      next_number += 1\n\n    injective_map_latex = (\n      semantic_map_latex(\n        injective_step\n      )\n    )\n    surjective_map_latex = (\n      semantic_map_latex(\n        surjective_step\n      )\n    )\n    isomorphism_line = (\n      _phase159_plain_map_property_line(\n        isomorphism_step,\n        "同型",\n      )\n    )\n\n    if (\n      injective_map_latex is None\n      or surjective_map_latex is None\n      or isomorphism_line is None\n    ):\n      continue\n\n    numbered_by_index[\n      injective_index\n    ] = (\n      injective_map_latex,\n      "単射",\n      injective_number,\n      (\n        id(\n          injective_step\n        )\n        in exactness_conclusion_step_ids\n      ),\n    )\n    numbered_by_index[\n      surjective_index\n    ] = (\n      surjective_map_latex,\n      "全射",\n      surjective_number,\n      (\n        id(\n          surjective_step\n        )\n        in exactness_conclusion_step_ids\n      ),\n    )\n    isomorphism_by_index[\n      isomorphism_index\n    ] = (\n      injective_number,\n      surjective_number,\n      isomorphism_line,\n    )\n\n  output_lines = []\n\n  def append_exactness_connector() -> None:\n    previous_nonblank = next(\n      (\n        line.strip()\n        for line in reversed(\n          output_lines\n        )\n        if line.strip()\n      ),\n      None,\n    )\n\n    if previous_nonblank == "完全性より,":\n      return\n\n    if (\n      output_lines\n      and output_lines[\n        -1\n      ].strip()\n    ):\n      output_lines.append(\n        ""\n      )\n\n    output_lines.extend(\n      (\n        "完全性より,",\n        "",\n      )\n    )\n\n  for index, line in enumerate(\n    lines\n  ):\n    numbered = numbered_by_index.get(\n      index\n    )\n\n    if numbered is not None:\n      (\n        map_latex,\n        property_label,\n        number,\n        uses_exactness,\n      ) = numbered\n\n      if uses_exactness:\n        append_exactness_connector()\n\n      output_lines.extend(\n        (\n          r"\\[",\n          (\n            map_latex\n            + r"\\quad\\text{は"\n            + property_label\n            + r"}. \\qquad ("\n            + str(\n              number\n            )\n            + ")"\n          ),\n          r"\\]",\n        )\n      )\n      continue\n\n    isomorphism = isomorphism_by_index.get(\n      index\n    )\n\n    if isomorphism is not None:\n      (\n        injective_number,\n        surjective_number,\n        isomorphism_line,\n      ) = isomorphism\n      output_lines.append(\n        (\n          "("\n          + str(\n            injective_number\n          )\n          + "), ("\n          + str(\n            surjective_number\n          )\n          + ") より, "\n          + isomorphism_line\n        )\n      )\n      continue\n\n    output_lines.append(\n      line\n    )\n\n  compacted = []\n  previous_blank = False\n\n  for line in output_lines:\n    is_blank = not line.strip()\n\n    if (\n      is_blank\n      and previous_blank\n    ):\n      continue\n\n    compacted.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return (\n    prefix\n    + "\\n".join(\n      compacted\n    )\n    + (\n      "\\n"\n      if rendered.endswith(\n        "\\n"\n      )\n      else ""\n    )\n  )\n'
TEST_REPAIR25 = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _generic_group_map_name,\n)\nfrom toda_group_proof_narrative_renderer import (\n  _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,\n  _phase159_recursive_map_property_triples,\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_reasons import (\n  build_toda_group_proof_narrative_reason_sidecar,\n  TodaGroupProofNarrativeReasonKind,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _presentation(\n  n: int,\n  k: int,\n):\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef test_phase159_repair25_pi3_2_exactness_reason_uses_semantic_map_name():\n  presentation = _presentation(\n    2,\n    1,\n  )\n  semantic_presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n  semantic_sidecar = (\n    build_toda_group_proof_narrative_semantic_sidecar(\n      semantic_presentation\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      semantic_presentation,\n      semantic_sidecar,\n    )\n  )\n\n  hopf_exactness_reasons = tuple(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n      and _generic_group_map_name(\n        getattr(\n          reason.conclusion_step.conclusion,\n          "map",\n          None,\n        )\n      )\n      == "H"\n    )\n  )\n\n  assert len(\n    hopf_exactness_reasons\n  ) == 2\n\n\ndef test_phase159_repair25_pi11_6_recursive_semantic_triple_exists():\n  presentation = _presentation(\n    6,\n    5,\n  )\n  triples = (\n    _phase159_recursive_map_property_triples(\n      presentation\n    )\n  )\n\n  hopf_triples = tuple(\n    triple\n    for triple in triples\n    if (\n      _generic_group_map_name(\n        getattr(\n          triple[\n            2\n          ].conclusion,\n          "map",\n          None,\n        )\n      )\n      == "H"\n      and getattr(\n        getattr(\n          triple[\n            2\n          ].conclusion,\n          "map",\n          None,\n        ),\n        "source_group",\n        None,\n      )\n      is not None\n    )\n  )\n\n  assert hopf_triples\n\n\ndef test_phase159_repair25_pi11_6_keeps_numbered_reasoning_without_prose_matching():\n  presentation = _presentation(\n    6,\n    5,\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  assert (\n    "\\\\[\\n"\n    r"H: \\pi_{7}^{3} \\to \\pi_{7}^{5}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    "\\\\[\\n"\n    r"H: \\pi_{7}^{3} \\to \\pi_{7}^{5}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    r"(1), (2) より, "\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は同型."\n    in rendered\n  )\n\n\ndef test_phase159_repair25_text_only_helper_still_refuses_semantic_inference():\n  rendered = (\n    "# Group proof narrative\\n\\n"\n    "## 証明\\n\\n"\n    "$F: A \\\\to B$ は単射.\\n"\n    "$F: A \\\\to B$ は全射.\\n"\n    "$F: A \\\\to B$ は同型.\\n\\n"\n    "□\\n"\n  )\n\n  normalized = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n\n  assert normalized == rendered\n'
REPLACEMENT_OLD_PI3_TEST = 'def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():\n  presentation = _phase159_r1_2_pi3_2_presentation()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  injective = (\n    "完全性より,\\n\\n"\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n    "\\n\\\\]"\n  )\n  surjective = (\n    "完全性より,\\n\\n"\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n    "\\n\\\\]"\n  )\n  isomorphism = (\n    r"(1), (2) より, "\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."\n  )\n\n  assert injective in rendered\n  assert surjective in rendered\n  assert isomorphism in rendered\n\n  assert rendered.index(\n    injective\n  ) < rendered.index(\n    surjective\n  ) < rendered.index(\n    isomorphism\n  )\n\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}\\tag{1}$ は単射."\n    not in rendered\n  )\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}\\tag{2}$ は全射."\n    not in rendered\n  )\n'
REPLACEMENT_GENERIC_TEST = 'def test_phase159_r1_7c_r4_numbered_reasoning_requires_semantic_presentation():\n  from toda_group_proof_narrative_renderer import (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,\n  )\n\n  rendered = (\n    "# Group proof narrative\\n\\n"\n    "## 証明対象\\n\\n"\n    "target\\n\\n"\n    "## 使用する結果\\n\\n"\n    "---\\n\\n"\n    "## 証明\\n\\n"\n    "完全性より, $F: A \\\\to B$ は単射.\\n"\n    "完全性より, $F: A \\\\to B$ は全射.\\n"\n    "$F: A \\\\to B$ は同型写像である.\\n\\n"\n    "□\\n"\n  )\n\n  normalized = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n\n  assert normalized == rendered\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  marker = "def " + function_name + "("
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_def = source.find(
    "\ndef ",
    start + len(marker),
  )

  if next_def < 0:
    end = len(source)
  else:
    end = next_def + 1

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[end:].lstrip("\n")
  )


def insert_before_function(
  source: str,
  before_name: str,
  addition: str,
) -> str:
  marker = "def " + before_name + "("
  index = source.find(marker)

  if index < 0:
    raise RuntimeError(
      "insertion anchor not found: "
      + before_name
    )

  return (
    source[:index]
    + addition.rstrip()
    + "\n\n"
    + source[index:]
  )


def main() -> int:
  for path in (
    RENDERER_PATH,
    PI3_TEST_PATH,
    NUMBERED_TEST_PATH,
  ):
    if not path.exists():
      raise RuntimeError(
        "required file not found: "
        + str(path)
      )

  renderer = RENDERER_PATH.read_text(
    encoding="utf-8-sig",
  )

  repair24_marker = (
    "presentation: TodaGroupProofPresentation | None = None"
  )

  if repair24_marker not in renderer:
    raise RuntimeError(
      "repair25 requires repair24 to be applied first"
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  for path in (
    RENDERER_PATH,
    PI3_TEST_PATH,
    NUMBERED_TEST_PATH,
  ):
    shutil.copy2(
      path,
      BACKUP_DIR / path.name,
    )

  recursive_name = (
    "_phase159_recursive_map_property_triples"
  )

  if (
    "def "
    + recursive_name
    + "("
    not in renderer
  ):
    renderer = insert_before_function(
      renderer,
      "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
      NEW_RECURSIVE_HELPER,
    )

  renderer = replace_function(
    renderer,
    "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
    NEW_NUMBERED,
  )

  RENDERER_PATH.write_text(
    renderer,
    encoding="utf-8",
  )

  pi3_test = PI3_TEST_PATH.read_text(
    encoding="utf-8-sig",
  )
  pi3_test = replace_function(
    pi3_test,
    "test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically",
    REPLACEMENT_OLD_PI3_TEST,
  )
  PI3_TEST_PATH.write_text(
    pi3_test,
    encoding="utf-8",
  )

  numbered_test = NUMBERED_TEST_PATH.read_text(
    encoding="utf-8-sig",
  )
  old_generic_name = (
    "test_phase159_r1_7c_r4_numbered_reasoning_is_general_not_pi11_hardcoded"
  )
  if (
    "def "
    + old_generic_name
    + "("
    in numbered_test
  ):
    numbered_test = replace_function(
      numbered_test,
      old_generic_name,
      REPLACEMENT_GENERIC_TEST,
    )
  elif (
    "def test_phase159_r1_7c_r4_numbered_reasoning_requires_semantic_presentation("
    not in numbered_test
  ):
    raise RuntimeError(
      "generic numbered-reasoning test not found"
    )

  NUMBERED_TEST_PATH.write_text(
    numbered_test,
    encoding="utf-8",
  )

  if REPAIR24_TEST_PATH.exists():
    REPAIR24_TEST_PATH.unlink()

  REPAIR25_TEST_PATH.write_text(
    TEST_REPAIR25,
    encoding="utf-8",
  )

  print(
    "Phase 159 semantic numbered-map-property reasoning repair25 applied."
  )
  print(
    "Modified: "
    + str(RENDERER_PATH)
  )
  print(
    "Modified: "
    + str(PI3_TEST_PATH)
  )
  print(
    "Modified: "
    + str(NUMBERED_TEST_PATH)
  )
  print(
    "Added: "
    + str(REPAIR25_TEST_PATH)
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
