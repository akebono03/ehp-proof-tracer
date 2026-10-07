from __future__ import annotations

from pathlib import Path
import shutil
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi3_2_visible_dependency_topological_order.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / "test_phase159_pi3_2_visible_dependency_topological_order.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase159_pi3_2_visible_dependency_topological_order_repair4_backup"
)


NEW_FUNCTION = 'def order_toda_group_proof_narrative_visible_step_dependencies(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    blocks,\n    tuple,\n  ):\n    raise TypeError(\n      "blocks must be a tuple"\n    )\n\n  if not isinstance(\n    semantic_sidecar,\n    TodaGroupProofNarrativeSemanticSidecar,\n  ):\n    raise TypeError(\n      "semantic_sidecar must be a "\n      "TodaGroupProofNarrativeSemanticSidecar"\n    )\n\n  if not isinstance(\n    arguments,\n    tuple,\n  ):\n    raise TypeError(\n      "arguments must be a tuple"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  if not paragraphs:\n    return markdown\n\n  def strip_leading_prose(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            stripped = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    prefixes = (\n      "以上より, ",\n      "したがって, ",\n      "これより, ",\n      "これらより, ",\n      "完全性より, ",\n    )\n\n    changed = True\n\n    while changed:\n      changed = False\n\n      for prefix in prefixes:\n        if stripped.startswith(\n          prefix\n        ):\n          stripped = stripped[\n            len(\n              prefix\n            ):\n          ]\n          changed = True\n          break\n\n    return stripped\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    return (\n      _phase157_r11_reference_statement_match_key(\n        strip_leading_prose(\n          paragraph\n        )\n      )\n    )\n\n  step_ids_by_key = {}\n\n  for node in presentation.nodes:\n    proof_step = node.proof_step\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      continue\n\n    key = (\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n    proof_step_id = id(\n      proof_step\n    )\n\n    step_ids_by_key.setdefault(\n      key,\n      set(),\n    ).add(\n      proof_step_id\n    )\n\n  paragraph_indices_by_step_id = {}\n\n  for paragraph_index, paragraph in enumerate(\n    paragraphs\n  ):\n    key = paragraph_match_key(\n      paragraph\n    )\n    step_ids = step_ids_by_key.get(\n      key,\n      set(),\n    )\n\n    if len(\n      step_ids\n    ) != 1:\n      continue\n\n    proof_step_id = next(\n      iter(\n        step_ids\n      )\n    )\n    paragraph_indices_by_step_id.setdefault(\n      proof_step_id,\n      [],\n    ).append(\n      paragraph_index\n    )\n\n  visible_index_by_step_id = {\n    proof_step_id: indices[0]\n    for proof_step_id, indices\n    in paragraph_indices_by_step_id.items()\n    if len(\n      indices\n    ) == 1\n  }\n\n  visible_step_ids = set(\n    visible_index_by_step_id\n  )\n\n  if len(\n    visible_step_ids\n  ) < 2:\n    return markdown\n\n  argument_indices_by_step_id = {}\n\n  for argument_index, argument in enumerate(\n    arguments\n  ):\n    local_body = (\n      extract_toda_group_proof_narrative_argument_local_body_blocks(\n        presentation,\n        blocks,\n        semantic_sidecar,\n        arguments,\n        argument_index,\n      )\n    )\n    local_step_ids = {\n      id(\n        proof_step\n      )\n      for block in local_body\n      for proof_step in block.steps\n    }\n    conclusion_step = (\n      extract_toda_group_proof_narrative_argument_conclusion_step(\n        argument\n      )\n    )\n\n    if conclusion_step is not None:\n      local_step_ids.add(\n        id(\n          conclusion_step\n        )\n      )\n\n    for proof_step_id in local_step_ids:\n      argument_indices_by_step_id.setdefault(\n        proof_step_id,\n        set(),\n      ).add(\n        argument_index\n      )\n\n  successors = {\n    proof_step_id: set()\n    for proof_step_id in visible_step_ids\n  }\n  indegree = {\n    proof_step_id: 0\n    for proof_step_id in visible_step_ids\n  }\n\n  for edge in presentation.edges:\n    premise_id = id(\n      edge.premise_step\n    )\n    consumer_id = id(\n      edge.parent_step\n    )\n\n    if (\n      premise_id\n      not in visible_step_ids\n      or consumer_id\n      not in visible_step_ids\n      or premise_id == consumer_id\n    ):\n      continue\n\n    premise_arguments = (\n      argument_indices_by_step_id.get(\n        premise_id,\n        set(),\n      )\n    )\n    consumer_arguments = (\n      argument_indices_by_step_id.get(\n        consumer_id,\n        set(),\n      )\n    )\n\n    if not (\n      premise_arguments\n      & consumer_arguments\n    ):\n      continue\n\n    if consumer_id in successors[\n      premise_id\n    ]:\n      continue\n\n    successors[\n      premise_id\n    ].add(\n      consumer_id\n    )\n    indegree[\n      consumer_id\n    ] += 1\n\n  if not any(\n    successors.values()\n  ):\n    return markdown\n\n  remaining = set(\n    visible_step_ids\n  )\n  ordered_step_ids = []\n\n  while remaining:\n    ready = [\n      proof_step_id\n      for proof_step_id in remaining\n      if indegree[\n        proof_step_id\n      ] == 0\n    ]\n\n    if not ready:\n      return markdown\n\n    ready.sort(\n      key=lambda proof_step_id: (\n        visible_index_by_step_id[\n          proof_step_id\n        ],\n      )\n    )\n    chosen = ready[\n      0\n    ]\n    ordered_step_ids.append(\n      chosen\n    )\n    remaining.remove(\n      chosen\n    )\n\n    for successor in successors[\n      chosen\n    ]:\n      if successor in remaining:\n        indegree[\n          successor\n        ] -= 1\n\n  current_step_ids = tuple(\n    sorted(\n      visible_step_ids,\n      key=lambda proof_step_id: (\n        visible_index_by_step_id[\n          proof_step_id\n        ]\n      ),\n    )\n  )\n  ordered_step_ids = tuple(\n    ordered_step_ids\n  )\n\n  if ordered_step_ids == current_step_ids:\n    return markdown\n\n  paragraph_slots = tuple(\n    visible_index_by_step_id[\n      proof_step_id\n    ]\n    for proof_step_id in current_step_ids\n  )\n  paragraph_by_step_id = {\n    proof_step_id: paragraphs[\n      visible_index_by_step_id[\n        proof_step_id\n      ]\n    ]\n    for proof_step_id in visible_step_ids\n  }\n  reordered = list(\n    paragraphs\n  )\n\n  for paragraph_index, proof_step_id in zip(\n    paragraph_slots,\n    ordered_step_ids,\n  ):\n    reordered[\n      paragraph_index\n    ] = paragraph_by_step_id[\n      proof_step_id\n    ]\n\n  return "\\n\\n".join(\n    reordered\n  )\n\n\n'


START = (
  "def order_toda_group_proof_narrative_visible_step_dependencies(\\n"
)
END = (
  "\\n\\ndef order_toda_group_proof_narrative_visible_relation_dependencies(\\n"
)


def fail(message: str) -> None:
  print(
    "ERROR:",
    message,
    file=sys.stderr,
  )
  raise SystemExit(
    1
  )


if not TARGET.exists():
  fail(
    f"target file not found: {TARGET}"
  )

source = TARGET.read_text(
  encoding="utf-8"
)

start_index = source.find(
  START
)
end_index = source.find(
  END,
  start_index,
)

if (
  start_index < 0
  or end_index < 0
):
  fail(
    "visible-step ordering function boundaries not found"
  )

source = (
  source[
    :start_index
  ]
  + NEW_FUNCTION
  + source[
    end_index + 2:
  ]
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
  source,
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
  "Applied Phase 159 pi3_2 visible dependency ordering repair4."
)
print(
  f"Backup: {backup_target}"
)
print(
  f"Test:   {TEST_TARGET}"
)
