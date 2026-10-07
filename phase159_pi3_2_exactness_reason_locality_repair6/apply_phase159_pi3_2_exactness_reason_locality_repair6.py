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
  / "phase159_pi3_2_exactness_reason_locality_repair6_backup"
)
FUNCTION_NAME = "_normalize_exactness_to_map_property_reason_prose"
REPLACEMENT = 'def _normalize_exactness_to_map_property_reason_prose(\n  markdown: str,\n  reason: TodaGroupProofNarrativeReason,\n) -> str:\n  if (\n    reason.kind\n    is not TodaGroupProofNarrativeReasonKind\n    .EXACTNESS_TO_MAP_PROPERTY\n  ):\n    return markdown\n\n  sentence = (\n    render_toda_group_proof_narrative_reason_sentence(\n      reason\n    )\n  )\n  if sentence is None:\n    return markdown\n\n  lines = sentence.splitlines()\n\n  while (\n    lines\n    and lines[-1].strip()\n    in {\n      "以上より,",\n      "したがって,",\n      "これより,",\n      "これらより,",\n    }\n  ):\n    lines.pop()\n\n  reason_body = "\\n".join(\n    lines\n  ).strip()\n\n  if not reason_body:\n    return markdown\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  prefixed_reason_body = (\n    "これより, "\n    + reason_body\n  )\n  matching_indices = tuple(\n    index\n    for index, paragraph in enumerate(\n      paragraphs\n    )\n    if paragraph.strip()\n    in {\n      reason_body,\n      prefixed_reason_body,\n    }\n  )\n\n  if len(matching_indices) != 1:\n    return markdown\n\n  reason_index = matching_indices[0]\n  reason_paragraph = paragraphs[\n    reason_index\n  ].strip()\n\n  if reason_paragraph == prefixed_reason_body:\n    paragraphs[\n      reason_index\n    ] = reason_body\n\n  if (\n    reason_index > 0\n    and paragraphs[\n      reason_index - 1\n    ].strip()\n    == "これより,"\n  ):\n    paragraphs.pop(\n      reason_index - 1\n    )\n    reason_index -= 1\n\n  def statement_match_key(\n    line: str,\n  ) -> str:\n    normalized = line.strip().rstrip(\n      ".,"\n    )\n    marker = r"\\tag{"\n\n    while True:\n      marker_index = normalized.find(\n        marker\n      )\n\n      if marker_index < 0:\n        break\n\n      number_start = (\n        marker_index\n        + len(\n          marker\n        )\n      )\n      number_end = normalized.find(\n        "}",\n        number_start,\n      )\n\n      if number_end < 0:\n        break\n\n      number_text = normalized[\n        number_start:\n        number_end\n      ]\n\n      if not number_text.isdigit():\n        break\n\n      normalized = (\n        normalized[\n          :marker_index\n        ]\n        + normalized[\n          number_end + 1:\n        ]\n      )\n\n    return normalized\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            stripped = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    for prefix in (\n      "完全性より, ",\n      "以上より, ",\n      "したがって, ",\n      "これより, ",\n      "これらより, ",\n    ):\n      if stripped.startswith(\n        prefix\n      ):\n        stripped = stripped[\n          len(\n            prefix\n          ):\n        ]\n        break\n\n    return statement_match_key(\n      stripped\n    )\n\n  visible_premise_indices = []\n\n  for premise_step in reason.premise_steps:\n    premise_line = (\n      _render_generic_narrative_step(\n        premise_step\n      )\n    )\n\n    if not premise_line:\n      continue\n\n    premise_key = statement_match_key(\n      premise_line\n    )\n    premise_matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if (\n        index != reason_index\n        and paragraph_match_key(\n          paragraph\n        )\n        == premise_key\n      )\n    )\n\n    if len(\n      premise_matches\n    ) != 1:\n      continue\n\n    visible_premise_indices.append(\n      premise_matches[\n        0\n      ]\n    )\n\n  if not visible_premise_indices:\n    return "\\n\\n".join(\n      paragraphs\n    )\n\n  latest_premise_index = max(\n    visible_premise_indices\n  )\n\n  if (\n    reason_index\n    == latest_premise_index + 1\n  ):\n    return "\\n\\n".join(\n      paragraphs\n    )\n\n  if reason_index <= latest_premise_index:\n    return "\\n\\n".join(\n      paragraphs\n    )\n\n  paragraph = paragraphs.pop(\n    reason_index\n  )\n\n  paragraphs.insert(\n    latest_premise_index + 1,\n    paragraph,\n  )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'


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

if not TEST_SOURCE.exists():
  fail(
    "test payload not found: "
    + str(
      TEST_SOURCE
    )
  )

source = TARGET.read_text(
  encoding="utf-8",
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
  "Applied Phase 159 pi3_2 exactness reason locality repair6."
)
print(
  f"Backup: {backup_target}"
)
print(
  f"Test:   {TEST_TARGET}"
)
