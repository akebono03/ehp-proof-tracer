from __future__ import annotations

from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent

RENDERER_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_renderer.py"
)

TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair24.py"
)

BACKUP_DIR = (
  Path(__file__).resolve().parent
  / "backup_before_apply"
)

REASON_IMPORT = 'from toda_group_proof_narrative_reasons import (\n  build_toda_group_proof_narrative_reason_sidecar,\n  TodaGroupProofNarrativeReasonKind,\n)\n'

NEW_HELPER = 'def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n  rendered: str,\n  presentation: TodaGroupProofPresentation | None = None,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  if (\n    presentation is not None\n    and not isinstance(\n      presentation,\n      TodaGroupProofPresentation,\n    )\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation or None"\n    )\n\n  if presentation is None:\n    return rendered\n\n  proof_marker = "## 証明\\n\\n"\n  marker_index = rendered.find(\n    proof_marker\n  )\n\n  if marker_index < 0:\n    return rendered\n\n  proof_start = (\n    marker_index\n    + len(\n      proof_marker\n    )\n  )\n  prefix = rendered[\n    :proof_start\n  ]\n  proof_body = rendered[\n    proof_start:\n  ]\n  lines = proof_body.splitlines()\n\n  (\n    semantic_presentation,\n    semantic_sidecar,\n    _primary_component,\n  ) = _phase159_public_semantic_projection_context(\n    presentation\n  )\n\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      semantic_presentation,\n      semantic_sidecar,\n    )\n  )\n  exactness_conclusion_step_ids = {\n    id(\n      reason.conclusion_step\n    )\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n    )\n  }\n\n  tag_pattern = re.compile(\n    r"\\\\tag\\{(\\d+)\\}"\n  )\n\n  existing_numbers = tuple(\n    int(\n      match.group(\n        1\n      )\n    )\n    for line in lines\n    for match in tag_pattern.finditer(\n      line\n    )\n  )\n  next_number = (\n    max(\n      existing_numbers,\n      default=0,\n    )\n    + 1\n  )\n\n  def semantic_map_latex(\n    proof_step: ProofStep,\n  ) -> str | None:\n    group_map = getattr(\n      proof_step.conclusion,\n      "map",\n      None,\n    )\n\n    if group_map is None:\n      return None\n\n    return (\n      _render_generic_narrative_group_map_latex(\n        group_map\n      )\n    )\n\n  def find_property_line(\n    proof_step: ProofStep,\n    property_label: str,\n  ) -> tuple[\n    int,\n    int | None,\n  ] | None:\n    map_latex = semantic_map_latex(\n      proof_step\n    )\n\n    if map_latex is None:\n      return None\n\n    prose_marker = (\n      "は"\n      + property_label\n    )\n    display_marker = (\n      r"\\text{は"\n      + property_label\n      + "}"\n    )\n\n    matches = []\n\n    for index, line in enumerate(\n      lines\n    ):\n      if map_latex not in line:\n        continue\n\n      if (\n        prose_marker not in line\n        and display_marker not in line\n      ):\n        continue\n\n      tag_match = tag_pattern.search(\n        line\n      )\n      matches.append(\n        (\n          index,\n          (\n            int(\n              tag_match.group(\n                1\n              )\n            )\n            if tag_match is not None\n            else None\n          ),\n        )\n      )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  def find_isomorphism_line(\n    proof_step: ProofStep,\n  ) -> int | None:\n    map_latex = semantic_map_latex(\n      proof_step\n    )\n\n    if map_latex is None:\n      return None\n\n    matches = [\n      index\n      for index, line in enumerate(\n        lines\n      )\n      if (\n        map_latex in line\n        and (\n          "は同型." in line\n          or "は同型写像." in line\n          or "は同型である." in line\n          or "は同型写像である." in line\n        )\n      )\n    ]\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  numbered_by_index = {}\n  isomorphism_by_index = {}\n\n  for (\n    injective_step,\n    surjective_step,\n    isomorphism_step,\n  ) in _phase159_public_map_property_triples(\n    semantic_presentation\n  ):\n    injective_row = find_property_line(\n      injective_step,\n      "単射",\n    )\n    surjective_row = find_property_line(\n      surjective_step,\n      "全射",\n    )\n    isomorphism_index = (\n      find_isomorphism_line(\n        isomorphism_step\n      )\n    )\n\n    if (\n      injective_row is None\n      or surjective_row is None\n      or isomorphism_index is None\n    ):\n      continue\n\n    (\n      injective_index,\n      injective_number,\n    ) = injective_row\n    (\n      surjective_index,\n      surjective_number,\n    ) = surjective_row\n\n    if injective_number is None:\n      injective_number = next_number\n      next_number += 1\n\n    if surjective_number is None:\n      surjective_number = next_number\n      next_number += 1\n\n    injective_map_latex = (\n      semantic_map_latex(\n        injective_step\n      )\n    )\n    surjective_map_latex = (\n      semantic_map_latex(\n        surjective_step\n      )\n    )\n    isomorphism_line = (\n      _phase159_plain_map_property_line(\n        isomorphism_step,\n        "同型",\n      )\n    )\n\n    if (\n      injective_map_latex is None\n      or surjective_map_latex is None\n      or isomorphism_line is None\n    ):\n      continue\n\n    numbered_by_index[\n      injective_index\n    ] = (\n      injective_map_latex,\n      "単射",\n      injective_number,\n      (\n        id(\n          injective_step\n        )\n        in exactness_conclusion_step_ids\n      ),\n    )\n    numbered_by_index[\n      surjective_index\n    ] = (\n      surjective_map_latex,\n      "全射",\n      surjective_number,\n      (\n        id(\n          surjective_step\n        )\n        in exactness_conclusion_step_ids\n      ),\n    )\n    isomorphism_by_index[\n      isomorphism_index\n    ] = (\n      injective_number,\n      surjective_number,\n      isomorphism_line,\n    )\n\n  output_lines = []\n\n  def append_exactness_connector() -> None:\n    previous_nonblank = next(\n      (\n        line.strip()\n        for line in reversed(\n          output_lines\n        )\n        if line.strip()\n      ),\n      None,\n    )\n\n    if previous_nonblank == "完全性より,":\n      return\n\n    if (\n      output_lines\n      and output_lines[\n        -1\n      ].strip()\n    ):\n      output_lines.append(\n        ""\n      )\n\n    output_lines.extend(\n      (\n        "完全性より,",\n        "",\n      )\n    )\n\n  for index, line in enumerate(\n    lines\n  ):\n    numbered = numbered_by_index.get(\n      index\n    )\n\n    if numbered is not None:\n      (\n        map_latex,\n        property_label,\n        number,\n        uses_exactness,\n      ) = numbered\n\n      if uses_exactness:\n        append_exactness_connector()\n\n      output_lines.extend(\n        (\n          r"\\[",\n          (\n            map_latex\n            + r"\\quad\\text{は"\n            + property_label\n            + r"}. \\qquad ("\n            + str(\n              number\n            )\n            + ")"\n          ),\n          r"\\]",\n        )\n      )\n      continue\n\n    isomorphism = isomorphism_by_index.get(\n      index\n    )\n\n    if isomorphism is not None:\n      (\n        injective_number,\n        surjective_number,\n        isomorphism_line,\n      ) = isomorphism\n      output_lines.append(\n        (\n          "("\n          + str(\n            injective_number\n          )\n          + "), ("\n          + str(\n            surjective_number\n          )\n          + ") より, "\n          + isomorphism_line\n        )\n      )\n      continue\n\n    output_lines.append(\n      line\n    )\n\n  compacted = []\n  previous_blank = False\n\n  for line in output_lines:\n    is_blank = not line.strip()\n\n    if (\n      is_blank\n      and previous_blank\n    ):\n      continue\n\n    compacted.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return (\n    prefix\n    + "\\n".join(\n      compacted\n    )\n    + (\n      "\\n"\n      if rendered.endswith(\n        "\\n"\n      )\n      else ""\n    )\n  )\n'

NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered,\n      presentation=presentation,\n    )\n  )\n\n  return (\n    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n      rendered\n    )\n  )\n'

TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_reasons import (\n  build_toda_group_proof_narrative_reason_sidecar,\n  TodaGroupProofNarrativeReasonKind,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _presentation(\n  n: int,\n  k: int,\n):\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef test_phase159_repair24_pi3_2_numbered_hopf_properties_keep_exactness_provenance():\n  presentation = _presentation(\n    2,\n    1,\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  injective = (\n    "完全性より,\\n\\n"\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n    "\\n\\\\]"\n  )\n  surjective = (\n    "完全性より,\\n\\n"\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n    "\\n\\\\]"\n  )\n  isomorphism = (\n    r"(1), (2) より, "\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."\n  )\n\n  assert injective in rendered\n  assert surjective in rendered\n  assert isomorphism in rendered\n\n  assert rendered.index(\n    injective\n  ) < rendered.index(\n    surjective\n  ) < rendered.index(\n    isomorphism\n  )\n\n\ndef test_phase159_repair24_pi3_2_exactness_connector_is_backed_by_typed_reason():\n  presentation = _presentation(\n    2,\n    1,\n  )\n  semantic_presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n  semantic_sidecar = (\n    build_toda_group_proof_narrative_semantic_sidecar(\n      semantic_presentation\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      semantic_presentation,\n      semantic_sidecar,\n    )\n  )\n\n  exactness_reasons = tuple(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n    )\n  )\n\n  hopf_reasons = tuple(\n    reason\n    for reason in exactness_reasons\n    if getattr(\n      getattr(\n        reason.conclusion_step.conclusion,\n        "map",\n        None,\n      ),\n      "name",\n      None,\n    )\n    == "H"\n  )\n\n  assert len(\n    hopf_reasons\n  ) >= 2\n\n\ndef test_phase159_repair24_text_only_helper_does_not_infer_semantics_from_prose():\n  rendered = (\n    "# Group proof narrative\\n\\n"\n    "## 証明\\n\\n"\n    "$F: A \\\\to B$ は単射.\\n"\n    "$F: A \\\\to B$ は全射.\\n"\n    "$F: A \\\\to B$ は同型.\\n\\n"\n    "□\\n"\n  )\n\n  normalized = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n\n  assert normalized == rendered\n\n\ndef test_phase159_repair24_pi11_6_numbered_hopf_reasoning_still_uses_semantic_pairing():\n  presentation = _presentation(\n    6,\n    5,\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  assert (\n    r"H: \\pi_{7}^{3} \\to \\pi_{7}^{5}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n    in rendered\n  )\n  assert (\n    r"H: \\pi_{7}^{3} \\to \\pi_{7}^{5}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n    in rendered\n  )\n  assert (\n    r"(1), (2) より, "\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は同型."\n    in rendered\n  )\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
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
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_def = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_def < 0:
    end = len(
      source
    )
  else:
    end = next_def + 1

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      end:
    ].lstrip(
      "\n"
    )
  )


def ensure_reason_import(
  source: str,
) -> str:
  import_marker = (
    "from toda_group_proof_narrative_reasons import ("
  )

  if import_marker in source:
    import_start = source.find(
      import_marker
    )
    import_end = source.find(
      ")",
      import_start,
    )

    if import_end < 0:
      raise RuntimeError(
        "unterminated toda_group_proof_narrative_reasons import"
      )

    import_block = source[
      import_start:
      import_end + 1
    ]
    required_names = (
      "build_toda_group_proof_narrative_reason_sidecar",
      "TodaGroupProofNarrativeReasonKind",
    )

    if all(
      name in import_block
      for name in required_names
    ):
      return source

    raise RuntimeError(
      "existing toda_group_proof_narrative_reasons import "
      "must be reviewed manually"
    )

  anchor = (
    "from toda_group_proof_narrative_semantics import (\n"
  )
  index = source.find(
    anchor
  )

  if index < 0:
    raise RuntimeError(
      "semantic import anchor not found"
    )

  return (
    source[
      :index
    ]
    + REASON_IMPORT
    + source[
      index:
    ]
  )


def main() -> int:
  if not RENDERER_PATH.exists():
    raise RuntimeError(
      "renderer not found: "
      + str(
        RENDERER_PATH
      )
    )

  source = RENDERER_PATH.read_text(
    encoding="utf-8-sig",
  )

  required_markers = (
    "def _phase159_public_map_property_triples(",
    "def _phase159_public_semantic_projection_context(",
    "def _phase159_plain_map_property_line(",
    "def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(",
    "def render_toda_group_proof_narrative_markdown(",
  )

  missing = [
    marker
    for marker in required_markers
    if marker not in source
  ]

  if missing:
    raise RuntimeError(
      "current renderer is outside repair24 prerequisites: "
      + ", ".join(
        missing
      )
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    RENDERER_PATH,
    BACKUP_DIR
    / RENDERER_PATH.name,
  )

  updated = ensure_reason_import(
    source
  )
  updated = replace_function(
    updated,
    "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
    NEW_HELPER,
  )
  updated = replace_function(
    updated,
    "render_toda_group_proof_narrative_markdown",
    NEW_RENDER,
  )

  RENDERER_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  TEST_PATH.write_text(
    TEST_SOURCE,
    encoding="utf-8",
  )

  print(
    "Phase 159 pi3_2 semantic numbered-map-property "
    "reasoning repair24 applied."
  )
  print(
    "Modified: "
    + str(
      RENDERER_PATH
    )
  )
  print(
    "Added: "
    + str(
      TEST_PATH
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
