from __future__ import annotations

from pathlib import Path
import shutil
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_renderer.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / "test_phase159_pi3_2_public_definition_premise_locality.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi3_2_public_definition_premise_locality.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase159_pi3_2_public_definition_premise_locality_repair18_backup"
)
HELPER_NAME = (
  "_phase159_order_public_unique_preimage_definition_premises"
)
HELPER = 'def _phase159_order_public_unique_preimage_definition_premises(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  proof_marker = "## 証明\\n\\n"\n  marker_index = rendered.find(\n    proof_marker\n  )\n\n  if marker_index < 0:\n    return rendered\n\n  proof_start = (\n    marker_index\n    + len(\n      proof_marker\n    )\n  )\n  prefix = rendered[\n    :proof_start\n  ]\n  proof_body = rendered[\n    proof_start:\n  ]\n  had_trailing_newline = rendered.endswith(\n    "\\n"\n  )\n  paragraphs = proof_body.rstrip(\n    "\\n"\n  ).split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for reference_prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            reference_prefix\n          ):\n            stripped = suffix[\n              len(\n                reference_prefix\n              ):\n            ]\n            break\n\n    for prose_prefix in (\n      "完全性より, ",\n      "以上より, ",\n      "したがって, ",\n      "これより, ",\n      "これらより, ",\n    ):\n      if stripped.startswith(\n        prose_prefix\n      ):\n        stripped = stripped[\n          len(\n            prose_prefix\n          ):\n        ]\n        break\n\n    for verbose, concise in (\n      (\n        " は単射である.",\n        " は単射.",\n      ),\n      (\n        " は全射である.",\n        " は全射.",\n      ),\n      (\n        " は零写像である.",\n        " は零写像.",\n      ),\n      (\n        " は同型写像である.",\n        " は同型.",\n      ),\n    ):\n      if stripped.endswith(\n        verbose\n      ):\n        stripped = (\n          stripped[\n            :-len(\n              verbose\n            )\n          ]\n          + concise\n        )\n        break\n\n    return stripped.rstrip(\n      ".,"\n    )\n\n  def paragraph_index_for_step(\n    proof_step: ProofStep,\n  ) -> int | None:\n    line = _render_generic_narrative_step(\n      proof_step\n    )\n\n    if not line:\n      return None\n\n    target_key = match_key(\n      line\n    )\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  for node in presentation.nodes:\n    proof_step = node.proof_step\n    definition_line = (\n      _phase159_unique_preimage_definition_line(\n        proof_step\n      )\n    )\n\n    if definition_line is None:\n      continue\n\n    definition_matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip()\n      == definition_line\n    )\n\n    if len(\n      definition_matches\n    ) != 1:\n      continue\n\n    visible_premise_records = tuple(\n      (\n        premise_step,\n        paragraph_index_for_step(\n          premise_step\n        ),\n      )\n      for premise_step in proof_step.premises\n    )\n\n    if any(\n      premise_index is None\n      for (\n        _,\n        premise_index,\n      ) in visible_premise_records\n    ):\n      continue\n\n    premise_indices = tuple(\n      premise_index\n      for (\n        _,\n        premise_index,\n      ) in visible_premise_records\n      if premise_index is not None\n    )\n\n    if len(\n      premise_indices\n    ) != len(\n      proof_step.premises\n    ):\n      continue\n\n    definition_index = definition_matches[\n      0\n    ]\n    expected_indices = tuple(\n      range(\n        definition_index\n        - len(\n          premise_indices\n        ),\n        definition_index,\n      )\n    )\n\n    if premise_indices == expected_indices:\n      continue\n\n    premise_paragraphs = tuple(\n      paragraphs[\n        premise_index\n      ]\n      for premise_index in premise_indices\n    )\n\n    for premise_index in sorted(\n      premise_indices,\n      reverse=True,\n    ):\n      paragraphs.pop(\n        premise_index\n      )\n\n    definition_matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip()\n      == definition_line\n    )\n\n    if len(\n      definition_matches\n    ) != 1:\n      continue\n\n    definition_index = definition_matches[\n      0\n    ]\n    paragraphs[\n      definition_index:\n      definition_index\n    ] = premise_paragraphs\n\n  result = (\n    prefix\n    + "\\n\\n".join(\n      paragraphs\n    )\n  )\n\n  if had_trailing_newline:\n    result += "\\n"\n\n  return result\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_order_public_unique_preimage_definition_premises(\n      presentation,\n      rendered,\n    )\n  )\n'


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
    + source[
      next_def + 1:
    ]
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

helper_marker = (
  "def "
  + HELPER_NAME
  + "("
)

if helper_marker not in source:
  render_marker = (
    "def render_toda_group_proof_narrative_markdown("
  )
  render_start = source.find(
    render_marker
  )

  if render_start < 0:
    fail(
      "render function insertion anchor not found"
    )

  source = (
    source[
      :render_start
    ]
    + HELPER.rstrip()
    + "\n\n\n"
    + source[
      render_start:
    ]
  )

updated = replace_top_level_function(
  source,
  "render_toda_group_proof_narrative_markdown",
  RENDER_FUNCTION,
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
  "Applied Phase 159 pi3_2 public definition-premise locality repair18."
)
print(
  "Backup: "
  + str(
    backup_target
  )
)
print(
  "Test:   "
  + str(
    TEST_TARGET
  )
)
