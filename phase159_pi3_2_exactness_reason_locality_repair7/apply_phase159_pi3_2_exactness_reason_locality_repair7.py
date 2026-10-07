from __future__ import annotations

from pathlib import Path
import shutil
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / "test_phase159_pi3_2_exactness_reason_locality.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi3_2_exactness_reason_locality.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase159_pi3_2_exactness_reason_locality_repair7_backup"
)
FUNCTION_NAME = (
  "order_toda_group_proof_narrative_injective_image_order_reason"
)
REPLACEMENT = 'def order_toda_group_proof_narrative_injective_image_order_reason(\n  markdown: str,\n  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reason_sidecar,\n    TodaGroupProofNarrativeReasonSidecar,\n  ):\n    raise TypeError(\n      "reason_sidecar must be a "\n      "TodaGroupProofNarrativeReasonSidecar"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def statement_match_key(\n    line: str,\n  ) -> str:\n    if not isinstance(\n      line,\n      str,\n    ):\n      raise TypeError(\n        "line must be a str"\n      )\n\n    normalized = line.strip().rstrip(\n      ".,"\n    )\n    marker = r"\\tag{"\n\n    while True:\n      marker_index = normalized.find(\n        marker\n      )\n\n      if marker_index < 0:\n        break\n\n      number_start = (\n        marker_index\n        + len(\n          marker\n        )\n      )\n      number_end = normalized.find(\n        "}",\n        number_start,\n      )\n\n      if number_end < 0:\n        break\n\n      number_text = normalized[\n        number_start:\n        number_end\n      ]\n\n      if not number_text.isdigit():\n        break\n\n      normalized = (\n        normalized[\n          :marker_index\n        ]\n        + normalized[\n          number_end + 1:\n        ]\n      )\n\n    return normalized\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            stripped = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    return statement_match_key(\n      stripped\n    )\n\n  def paragraph_index_for_step(\n    proof_step,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = statement_match_key(\n      rendered\n    )\n\n    matching = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph_match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matching\n    ) != 1:\n      return None\n\n    return matching[\n      0\n    ]\n\n  def visible_reason_paragraph(\n    reason: TodaGroupProofNarrativeReason,\n  ) -> str | None:\n    sentence = (\n      render_toda_group_proof_narrative_reason_sentence(\n        reason\n      )\n    )\n\n    if sentence is None:\n      return None\n\n    lines = sentence.splitlines()\n\n    while (\n      lines\n      and lines[\n        -1\n      ].strip()\n      in {\n        "以上より,",\n        "したがって,",\n        "これより,",\n        "これらより,",\n      }\n    ):\n      lines.pop()\n\n    rendered = "\\n".join(\n      lines\n    ).strip()\n\n    return (\n      rendered\n      if rendered\n      else None\n    )\n\n  for reason in reason_sidecar.reasons:\n    if (\n      reason.kind\n      is not TodaGroupProofNarrativeReasonKind\n      .INJECTIVE_IMAGE_ORDER\n    ):\n      continue\n\n    reason_paragraph = (\n      visible_reason_paragraph(\n        reason\n      )\n    )\n\n    if reason_paragraph is None:\n      continue\n\n    reason_indices = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip()\n      == reason_paragraph\n    )\n\n    if len(\n      reason_indices\n    ) != 1:\n      continue\n\n    conclusion_index = (\n      paragraph_index_for_step(\n        reason.conclusion_step\n      )\n    )\n\n    if conclusion_index is None:\n      continue\n\n    premise_indices = tuple(\n      index\n      for premise in reason.premise_steps\n      for index in (\n        paragraph_index_for_step(\n          premise\n        ),\n      )\n      if index is not None\n    )\n\n    if len(\n      premise_indices\n    ) != len(\n      reason.premise_steps\n    ):\n      continue\n\n    if max(\n      premise_indices\n    ) >= conclusion_index:\n      continue\n\n    reason_index = reason_indices[\n      0\n    ]\n\n    if (\n      reason_index\n      == conclusion_index - 1\n      and reason_index\n      > max(\n        premise_indices\n      )\n    ):\n      continue\n\n    paragraph = paragraphs.pop(\n      reason_index\n    )\n\n    conclusion_index = (\n      paragraph_index_for_step(\n        reason.conclusion_step\n      )\n    )\n\n    if conclusion_index is None:\n      paragraphs.insert(\n        reason_index,\n        paragraph,\n      )\n      continue\n\n    paragraphs.insert(\n      conclusion_index,\n      paragraph,\n    )\n\n  def map_identity(\n    proof_step,\n  ):\n    statement = getattr(\n      proof_step,\n      "conclusion",\n      None,\n    )\n\n    return getattr(\n      statement,\n      "map",\n      None,\n    )\n\n  def visible_reason_index(\n    reason: TodaGroupProofNarrativeReason,\n  ) -> int | None:\n    reason_paragraph = (\n      visible_reason_paragraph(\n        reason\n      )\n    )\n\n    if reason_paragraph is None:\n      return None\n\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip()\n      == reason_paragraph\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  connector_paragraphs = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  for node in reason_sidecar.presentation.nodes:\n    isomorphism_step = node.proof_step\n    isomorphism_line = (\n      _render_generic_narrative_step(\n        isomorphism_step\n      )\n    )\n\n    if (\n      not isomorphism_line\n      or "は同型写像である."\n      not in isomorphism_line\n    ):\n      continue\n\n    isomorphism_map = map_identity(\n      isomorphism_step\n    )\n\n    if isomorphism_map is None:\n      continue\n\n    injective_indices = []\n    surjective_indices = []\n\n    for reason in reason_sidecar.reasons:\n      conclusion_step = reason.conclusion_step\n\n      if map_identity(\n        conclusion_step\n      ) != isomorphism_map:\n        continue\n\n      conclusion_line = (\n        _render_generic_narrative_step(\n          conclusion_step\n        )\n      )\n\n      if not conclusion_line:\n        continue\n\n      reason_index = visible_reason_index(\n        reason\n      )\n\n      if reason_index is None:\n        continue\n\n      if "は単射である." in conclusion_line:\n        injective_indices.append(\n          reason_index\n        )\n        continue\n\n      if "は全射である." in conclusion_line:\n        surjective_indices.append(\n          reason_index\n        )\n\n    if (\n      not injective_indices\n      or not surjective_indices\n    ):\n      continue\n\n    isomorphism_index = (\n      paragraph_index_for_step(\n        isomorphism_step\n      )\n    )\n\n    if isomorphism_index is None:\n      continue\n\n    latest_support_index = max(\n      (\n        *injective_indices,\n        *surjective_indices,\n      )\n    )\n\n    if isomorphism_index > latest_support_index:\n      continue\n\n    block_start = isomorphism_index\n\n    if (\n      block_start > 0\n      and paragraphs[\n        block_start - 1\n      ].strip()\n      in connector_paragraphs\n    ):\n      block_start -= 1\n\n    block = paragraphs[\n      block_start:\n      isomorphism_index + 1\n    ]\n\n    del paragraphs[\n      block_start:\n      isomorphism_index + 1\n    ]\n\n    injective_indices = []\n    surjective_indices = []\n\n    for reason in reason_sidecar.reasons:\n      conclusion_step = reason.conclusion_step\n\n      if map_identity(\n        conclusion_step\n      ) != isomorphism_map:\n        continue\n\n      conclusion_line = (\n        _render_generic_narrative_step(\n          conclusion_step\n        )\n      )\n\n      if not conclusion_line:\n        continue\n\n      reason_index = visible_reason_index(\n        reason\n      )\n\n      if reason_index is None:\n        continue\n\n      if "は単射である." in conclusion_line:\n        injective_indices.append(\n          reason_index\n        )\n        continue\n\n      if "は全射である." in conclusion_line:\n        surjective_indices.append(\n          reason_index\n        )\n\n    if (\n      not injective_indices\n      or not surjective_indices\n    ):\n      paragraphs[\n        block_start:\n        block_start\n      ] = block\n      continue\n\n    insertion_index = (\n      max(\n        (\n          *injective_indices,\n          *surjective_indices,\n        )\n      )\n      + 1\n    )\n\n    paragraphs[\n      insertion_index:\n      insertion_index\n    ] = block\n\n  rendered = "\\n\\n".join(\n    paragraphs\n  )\n\n  for reason in reason_sidecar.reasons:\n    rendered = (\n      _normalize_exactness_to_map_property_reason_prose(\n        rendered,\n        reason,\n      )\n    )\n\n  return rendered\n'


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


if not TARGET.exists():
  fail(
    "target file not found: "
    + str(
      TARGET
    )
  )

source = TARGET.read_text(
  encoding="utf-8",
)

if (
  "def _normalize_exactness_to_map_property_reason_prose("
  not in source
):
  fail(
    "repair6 exactness normalization function not found"
  )

updated = replace_top_level_function(
  source,
  FUNCTION_NAME,
  REPLACEMENT,
)

BACKUP_DIR.mkdir(
  parents=True,
  exist_ok=True,
)

backup_target = (
  BACKUP_DIR
  / TARGET.name
)

if not backup_target.exists():
  shutil.copy2(
    TARGET,
    backup_target,
  )

TARGET.write_text(
  updated,
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
  "Applied Phase 159 pi3_2 exactness reason locality repair7."
)
print(
  f"Backup: {backup_target}"
)
print(
  f"Test:   {TEST_TARGET}"
)
