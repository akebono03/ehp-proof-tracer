from __future__ import annotations

from pathlib import Path
import shutil
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

REASON_RENDERER = (
  REPO_ROOT
  / "toda_group_proof_narrative_reason_renderer.py"
)
CONTRIBUTION_RENDERER = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / "test_phase159_pi3_2_final_locality_reapply.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi3_2_final_locality_reapply.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase159_pi3_2_final_locality_reapply_repair14_backup"
)

FUNCTION_NAME = (
  "order_toda_group_proof_narrative_injective_image_order_reason"
)
REPLACEMENT = 'def order_toda_group_proof_narrative_injective_image_order_reason(\n  markdown: str,\n  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reason_sidecar,\n    TodaGroupProofNarrativeReasonSidecar,\n  ):\n    raise TypeError(\n      "reason_sidecar must be a "\n      "TodaGroupProofNarrativeReasonSidecar"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def statement_match_key(\n    line: str,\n  ) -> str:\n    if not isinstance(\n      line,\n      str,\n    ):\n      raise TypeError(\n        "line must be a str"\n      )\n\n    normalized = line.strip().rstrip(\n      ".,"\n    )\n    marker = r"\\tag{"\n\n    while True:\n      marker_index = normalized.find(\n        marker\n      )\n\n      if marker_index < 0:\n        break\n\n      number_start = (\n        marker_index\n        + len(\n          marker\n        )\n      )\n      number_end = normalized.find(\n        "}",\n        number_start,\n      )\n\n      if number_end < 0:\n        break\n\n      number_text = normalized[\n        number_start:\n        number_end\n      ]\n\n      if not number_text.isdigit():\n        break\n\n      normalized = (\n        normalized[\n          :marker_index\n        ]\n        + normalized[\n          number_end + 1:\n        ]\n      )\n\n    return normalized\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            stripped = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    return statement_match_key(\n      stripped\n    )\n\n  def paragraph_index_for_step(\n    proof_step,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = statement_match_key(\n      rendered\n    )\n\n    matching = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph_match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matching\n    ) != 1:\n      return None\n\n    return matching[\n      0\n    ]\n\n  def visible_reason_paragraph(\n    reason: TodaGroupProofNarrativeReason,\n  ) -> str | None:\n    sentence = (\n      render_toda_group_proof_narrative_reason_sentence(\n        reason\n      )\n    )\n\n    if sentence is None:\n      return None\n\n    lines = sentence.splitlines()\n\n    while (\n      lines\n      and lines[\n        -1\n      ].strip()\n      in {\n        "以上より,",\n        "したがって,",\n        "これより,",\n        "これらより,",\n      }\n    ):\n      lines.pop()\n\n    rendered = "\\n".join(\n      lines\n    ).strip()\n\n    return (\n      rendered\n      if rendered\n      else None\n    )\n\n  for reason in reason_sidecar.reasons:\n    if (\n      reason.kind\n      is not TodaGroupProofNarrativeReasonKind\n      .INJECTIVE_IMAGE_ORDER\n    ):\n      continue\n\n    reason_paragraph = (\n      visible_reason_paragraph(\n        reason\n      )\n    )\n\n    if reason_paragraph is None:\n      continue\n\n    reason_indices = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip()\n      == reason_paragraph\n    )\n\n    if len(\n      reason_indices\n    ) != 1:\n      continue\n\n    conclusion_index = (\n      paragraph_index_for_step(\n        reason.conclusion_step\n      )\n    )\n\n    if conclusion_index is None:\n      continue\n\n    premise_indices = tuple(\n      index\n      for premise in reason.premise_steps\n      for index in (\n        paragraph_index_for_step(\n          premise\n        ),\n      )\n      if index is not None\n    )\n\n    if len(\n      premise_indices\n    ) != len(\n      reason.premise_steps\n    ):\n      continue\n\n    if max(\n      premise_indices\n    ) >= conclusion_index:\n      continue\n\n    reason_index = reason_indices[\n      0\n    ]\n\n    if (\n      reason_index\n      == conclusion_index - 1\n      and reason_index\n      > max(\n        premise_indices\n      )\n    ):\n      continue\n\n    paragraph = paragraphs.pop(\n      reason_index\n    )\n\n    conclusion_index = (\n      paragraph_index_for_step(\n        reason.conclusion_step\n      )\n    )\n\n    if conclusion_index is None:\n      paragraphs.insert(\n        reason_index,\n        paragraph,\n      )\n      continue\n\n    paragraphs.insert(\n      conclusion_index,\n      paragraph,\n    )\n\n  def map_identity(\n    proof_step,\n  ):\n    statement = getattr(\n      proof_step,\n      "conclusion",\n      None,\n    )\n\n    return getattr(\n      statement,\n      "map",\n      None,\n    )\n\n  def visible_reason_index(\n    reason: TodaGroupProofNarrativeReason,\n  ) -> int | None:\n    reason_paragraph = (\n      visible_reason_paragraph(\n        reason\n      )\n    )\n\n    if reason_paragraph is None:\n      return None\n\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip()\n      == reason_paragraph\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  connector_paragraphs = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  for node in reason_sidecar.presentation.nodes:\n    isomorphism_step = node.proof_step\n    isomorphism_line = (\n      _render_generic_narrative_step(\n        isomorphism_step\n      )\n    )\n\n    if (\n      not isomorphism_line\n      or "は同型写像である."\n      not in isomorphism_line\n    ):\n      continue\n\n    isomorphism_map = map_identity(\n      isomorphism_step\n    )\n\n    if isomorphism_map is None:\n      continue\n\n    injective_indices = []\n    surjective_indices = []\n\n    for reason in reason_sidecar.reasons:\n      conclusion_step = reason.conclusion_step\n\n      if map_identity(\n        conclusion_step\n      ) != isomorphism_map:\n        continue\n\n      conclusion_line = (\n        _render_generic_narrative_step(\n          conclusion_step\n        )\n      )\n\n      if not conclusion_line:\n        continue\n\n      reason_index = visible_reason_index(\n        reason\n      )\n\n      if reason_index is None:\n        continue\n\n      if "は単射である." in conclusion_line:\n        injective_indices.append(\n          reason_index\n        )\n        continue\n\n      if "は全射である." in conclusion_line:\n        surjective_indices.append(\n          reason_index\n        )\n\n    if (\n      not injective_indices\n      or not surjective_indices\n    ):\n      continue\n\n    isomorphism_index = (\n      paragraph_index_for_step(\n        isomorphism_step\n      )\n    )\n\n    if isomorphism_index is None:\n      continue\n\n    latest_support_index = max(\n      (\n        *injective_indices,\n        *surjective_indices,\n      )\n    )\n\n    if isomorphism_index > latest_support_index:\n      continue\n\n    block_start = isomorphism_index\n\n    if (\n      block_start > 0\n      and paragraphs[\n        block_start - 1\n      ].strip()\n      in connector_paragraphs\n    ):\n      block_start -= 1\n\n    block = paragraphs[\n      block_start:\n      isomorphism_index + 1\n    ]\n\n    del paragraphs[\n      block_start:\n      isomorphism_index + 1\n    ]\n\n    injective_indices = []\n    surjective_indices = []\n\n    for reason in reason_sidecar.reasons:\n      conclusion_step = reason.conclusion_step\n\n      if map_identity(\n        conclusion_step\n      ) != isomorphism_map:\n        continue\n\n      conclusion_line = (\n        _render_generic_narrative_step(\n          conclusion_step\n        )\n      )\n\n      if not conclusion_line:\n        continue\n\n      reason_index = visible_reason_index(\n        reason\n      )\n\n      if reason_index is None:\n        continue\n\n      if "は単射である." in conclusion_line:\n        injective_indices.append(\n          reason_index\n        )\n        continue\n\n      if "は全射である." in conclusion_line:\n        surjective_indices.append(\n          reason_index\n        )\n\n    if (\n      not injective_indices\n      or not surjective_indices\n    ):\n      paragraphs[\n        block_start:\n        block_start\n      ] = block\n      continue\n\n    insertion_index = (\n      max(\n        (\n          *injective_indices,\n          *surjective_indices,\n        )\n      )\n      + 1\n    )\n\n    paragraphs[\n      insertion_index:\n      insertion_index\n    ] = block\n\n  rendered = "\\n\\n".join(\n    paragraphs\n  )\n  paragraphs = rendered.split(\n    "\\n\\n"\n  )\n\n  def locality_match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            stripped = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    for prefix in (\n      "完全性より, ",\n      "以上より, ",\n      "したがって, ",\n      "これより, ",\n      "これらより, ",\n    ):\n      if stripped.startswith(\n        prefix\n      ):\n        stripped = stripped[\n          len(\n            prefix\n          ):\n        ]\n        break\n\n    for verbose, concise in (\n      (\n        " は単射である.",\n        " は単射.",\n      ),\n      (\n        " は全射である.",\n        " は全射.",\n      ),\n      (\n        " は零写像である.",\n        " は零写像.",\n      ),\n      (\n        " は同型写像である.",\n        " は同型.",\n      ),\n    ):\n      if stripped.endswith(\n        verbose\n      ):\n        stripped = (\n          stripped[\n            :-len(\n              verbose\n            )\n          ]\n          + concise\n        )\n        break\n\n    return statement_match_key(\n      stripped\n    )\n\n  def paragraph_index_for_line(\n    line: str,\n  ) -> int | None:\n    target_key = locality_match_key(\n      line\n    )\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if locality_match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  for reason in reason_sidecar.reasons:\n    if (\n      reason.kind\n      is not TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n    ):\n      continue\n\n    reason_paragraph = (\n      visible_reason_paragraph(\n        reason\n      )\n    )\n\n    if reason_paragraph is None:\n      continue\n\n    conclusion_matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip()\n      == reason_paragraph\n    )\n\n    if len(\n      conclusion_matches\n    ) != 1:\n      continue\n\n    conclusion_index = conclusion_matches[\n      0\n    ]\n    visible_premise_indices = []\n\n    for premise_step in reason.premise_steps:\n      premise_line = (\n        _render_generic_narrative_step(\n          premise_step\n        )\n      )\n\n      if not premise_line:\n        continue\n\n      premise_index = paragraph_index_for_line(\n        premise_line\n      )\n\n      if premise_index is None:\n        continue\n\n      visible_premise_indices.append(\n        premise_index\n      )\n\n    if not visible_premise_indices:\n      continue\n\n    latest_premise_index = max(\n      visible_premise_indices\n    )\n\n    if (\n      conclusion_index\n      <= latest_premise_index\n      or conclusion_index\n      == latest_premise_index + 1\n    ):\n      continue\n\n    paragraph = paragraphs.pop(\n      conclusion_index\n    )\n    paragraphs.insert(\n      latest_premise_index + 1,\n      paragraph,\n    )\n\n  def math_spans(\n    text: str,\n  ) -> tuple[\n    str,\n    ...,\n  ]:\n    spans = []\n    search_start = 0\n\n    while True:\n      open_index = text.find(\n        "$",\n        search_start,\n      )\n\n      if open_index < 0:\n        break\n\n      close_index = text.find(\n        "$",\n        open_index + 1,\n      )\n\n      if close_index < 0:\n        break\n\n      spans.append(\n        text[\n          open_index:\n          close_index + 1\n        ]\n      )\n      search_start = close_index + 1\n\n    return tuple(\n      spans\n    )\n\n  for node in reason_sidecar.presentation.nodes:\n    proof_step = node.proof_step\n    generic_definition = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not generic_definition:\n      continue\n\n    if (\n      "を満たす" not in generic_definition\n      or "を定める." not in generic_definition\n    ):\n      continue\n\n    premise_lines = tuple(\n      _render_generic_narrative_step(\n        premise_step\n      )\n      for premise_step in proof_step.premises\n    )\n    isomorphism_premises = tuple(\n      premise_line\n      for premise_line in premise_lines\n      if (\n        premise_line\n        and "同型写像である."\n        in premise_line\n      )\n    )\n\n    if len(\n      isomorphism_premises\n    ) != 1:\n      continue\n\n    definition_spans = math_spans(\n      generic_definition\n    )\n\n    if not definition_spans:\n      continue\n\n    definition_matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if (\n        paragraph.strip().startswith(\n          "この同型写像により, "\n        )\n        and all(\n          span in paragraph\n          for span in definition_spans\n        )\n      )\n    )\n\n    if len(\n      definition_matches\n    ) != 1:\n      continue\n\n    visible_premise_records = []\n\n    for premise_step in proof_step.premises:\n      premise_line = (\n        _render_generic_narrative_step(\n          premise_step\n        )\n      )\n\n      if not premise_line:\n        continue\n\n      premise_index = paragraph_index_for_line(\n        premise_line\n      )\n\n      if premise_index is None:\n        continue\n\n      visible_premise_records.append(\n        (\n          premise_step,\n          premise_index,\n        )\n      )\n\n    if not visible_premise_records:\n      continue\n\n    premise_paragraphs = [\n      paragraphs[\n        premise_index\n      ]\n      for (\n        _,\n        premise_index,\n      ) in visible_premise_records\n    ]\n\n    for premise_index in sorted(\n      (\n        premise_index\n        for (\n          _,\n          premise_index,\n        ) in visible_premise_records\n      ),\n      reverse=True,\n    ):\n      paragraphs.pop(\n        premise_index\n      )\n\n    definition_matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if (\n        paragraph.strip().startswith(\n          "この同型写像により, "\n        )\n        and all(\n          span in paragraph\n          for span in definition_spans\n        )\n      )\n    )\n\n    if len(\n      definition_matches\n    ) != 1:\n      continue\n\n    definition_index = definition_matches[\n      0\n    ]\n\n    paragraphs[\n      definition_index:\n      definition_index\n    ] = premise_paragraphs\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
CALL_ANCHOR = '  rendered = (\n    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n      rendered\n    )\n  )\n\n  generic_used_step_ids = (\n'
CALL_REPLACEMENT = '  rendered = (\n    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n      rendered\n    )\n  )\n  rendered = (\n    order_toda_group_proof_narrative_injective_image_order_reason(\n      rendered,\n      reason_sidecar,\n    )\n  )\n\n  generic_used_step_ids = (\n'


def fail(
  message: str,
) -> None:
  print(
    "ERROR:",
    message,
    file=sys.stderr,
  )
  raise SystemExit(
    1
  )


def replace_top_level_function(
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
    fail(
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
    return (
      source[:start]
      + replacement.rstrip()
      + "\n"
    )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[next_def + 1:]
  )


for target in (
  REASON_RENDERER,
  CONTRIBUTION_RENDERER,
):
  if not target.exists():
    fail(
      "target file not found: "
      + str(
        target
      )
    )

BACKUP_DIR.mkdir(
  parents=True,
  exist_ok=True,
)

for target in (
  REASON_RENDERER,
  CONTRIBUTION_RENDERER,
):
  backup_target = (
    BACKUP_DIR
    / target.name
  )

  if not backup_target.exists():
    shutil.copy2(
      target,
      backup_target,
    )

reason_source = REASON_RENDERER.read_text(
  encoding="utf-8",
)
reason_updated = replace_top_level_function(
  reason_source,
  FUNCTION_NAME,
  REPLACEMENT,
)
REASON_RENDERER.write_text(
  reason_updated,
  encoding="utf-8",
)

contribution_source = CONTRIBUTION_RENDERER.read_text(
  encoding="utf-8",
)

if CALL_REPLACEMENT in contribution_source:
  contribution_updated = contribution_source
elif CALL_ANCHOR in contribution_source:
  contribution_updated = contribution_source.replace(
    CALL_ANCHOR,
    CALL_REPLACEMENT,
    1,
  )
else:
  fail(
    "final re-apply call anchor not found"
  )

CONTRIBUTION_RENDERER.write_text(
  contribution_updated,
  encoding="utf-8",
)

TEST_TARGET.parent.mkdir(
  parents=True,
  exist_ok=True,
)
shutil.copy2(
  TEST_SOURCE,
  TEST_TARGET,
)

print(
  "Applied Phase 159 pi3_2 final locality re-apply repair14."
)
print(
  "Reason backup: "
  + str(
    BACKUP_DIR
    / REASON_RENDERER.name
  )
)
print(
  "Contribution backup: "
  + str(
    BACKUP_DIR
    / CONTRIBUTION_RENDERER.name
  )
)
print(
  "Test: "
  + str(
    TEST_TARGET
  )
)
