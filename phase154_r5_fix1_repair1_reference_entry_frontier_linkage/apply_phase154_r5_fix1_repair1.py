from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
BACKUP = (
  REPO_ROOT
  / "phase154_r5_fix1_repair1_reference_entry_frontier_linkage"
  / "backup_before_repair1"
  / TARGET.name
)

HELPERS = 'def _phase154_r5_reference_source_steps_by_number(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> dict[\n  int,\n  tuple[\n    ProofStep,\n    ...,\n  ],\n]:\n  source_steps_by_number = {}\n\n  for entry in reference_entries:\n    candidate_steps = []\n    seen_rendered_statements = set()\n\n    for proof_step in entry.proof_steps:\n      rendered_statement = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if not rendered_statement:\n        continue\n\n      if rendered_statement in seen_rendered_statements:\n        continue\n\n      seen_rendered_statements.add(\n        rendered_statement\n      )\n      candidate_steps.append(\n        proof_step\n      )\n\n    selected_steps = (\n      select_toda_group_proof_narrative_reference_statement_steps(\n        entry,\n        tuple(\n          candidate_steps\n        ),\n        presentation.edges,\n        root_step=presentation.root_step,\n      )\n    )\n\n    ordered_source_steps = []\n    seen_step_ids = set()\n\n    for proof_step in (\n      *selected_steps,\n      *entry.proof_steps,\n    ):\n      proof_step_id = id(\n        proof_step\n      )\n\n      if proof_step_id in seen_step_ids:\n        continue\n\n      seen_step_ids.add(\n        proof_step_id\n      )\n      ordered_source_steps.append(\n        proof_step\n      )\n\n    if ordered_source_steps:\n      source_steps_by_number[\n        entry.number\n      ] = tuple(\n        ordered_source_steps\n      )\n\n  return source_steps_by_number\n\n\ndef _phase154_r5_unique_visible_non_root_consumer_line(\n  presentation: TodaGroupProofPresentation,\n  source_steps: tuple[\n    ProofStep,\n    ...,\n  ],\n  body_markdown: str,\n) -> str | None:\n  if not source_steps:\n    return None\n\n  source_step_ids = {\n    id(\n      source_step\n    )\n    for source_step in source_steps\n  }\n  children_by_step_id = {}\n\n  for edge in presentation.edges:\n    children_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  queue = deque(\n    (\n      source_step,\n      0,\n    )\n    for source_step in source_steps\n  )\n  visited_distance_by_step_id = {}\n  visible_by_distance = {}\n\n  while queue:\n    current_step, distance = queue.popleft()\n    current_step_id = id(\n      current_step\n    )\n    known_distance = visited_distance_by_step_id.get(\n      current_step_id\n    )\n\n    if (\n      known_distance is not None\n      and known_distance <= distance\n    ):\n      continue\n\n    visited_distance_by_step_id[\n      current_step_id\n    ] = distance\n\n    for child_step in children_by_step_id.get(\n      current_step_id,\n      (),\n    ):\n      child_step_id = id(\n        child_step\n      )\n      child_distance = distance + 1\n\n      if child_step_id in source_step_ids:\n        queue.append(\n          (\n            child_step,\n            child_distance,\n          )\n        )\n        continue\n\n      if child_step is presentation.root_step:\n        continue\n\n      rendered_child = (\n        _render_generic_narrative_step(\n          child_step\n        )\n      )\n\n      if (\n        rendered_child\n        and rendered_child in body_markdown\n      ):\n        visible_by_distance.setdefault(\n          child_distance,\n          [],\n        ).append(\n          rendered_child\n        )\n        continue\n\n      queue.append(\n        (\n          child_step,\n          child_distance,\n        )\n      )\n\n  if not visible_by_distance:\n    return None\n\n  nearest_distance = min(\n    visible_by_distance\n  )\n  nearest_lines = tuple(\n    dict.fromkeys(\n      visible_by_distance[\n        nearest_distance\n      ]\n    )\n  )\n\n  if len(\n    nearest_lines\n  ) != 1:\n    return None\n\n  return nearest_lines[\n    0\n  ]\n\n\ndef link_toda_group_proof_narrative_reference_body_consumers(\n  presentation: TodaGroupProofPresentation,\n  body_markdown: str,\n  reference_entries,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  source_steps_by_number = (\n    _phase154_r5_reference_source_steps_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  lines = body_markdown.splitlines()\n\n  for reference_number, source_steps in (\n    source_steps_by_number.items()\n  ):\n    marker = (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]"\n    )\n\n    marker_indices = tuple(\n      index\n      for index, line in enumerate(\n        lines\n      )\n      if (\n        marker in line\n        and line.rstrip().endswith(\n          marker\n          + "を用いる。"\n        )\n      )\n    )\n\n    if len(\n      marker_indices\n    ) != 1:\n      continue\n\n    current_body = "\\n".join(\n      lines\n    )\n    consumer_line = (\n      _phase154_r5_unique_visible_non_root_consumer_line(\n        presentation,\n        source_steps,\n        current_body,\n      )\n    )\n\n    if consumer_line is None:\n      continue\n\n    consumer_indices = tuple(\n      index\n      for index, line in enumerate(\n        lines\n      )\n      if (\n        index != marker_indices[0]\n        and consumer_line in line\n      )\n    )\n\n    if len(\n      consumer_indices\n    ) != 1:\n      continue\n\n    marker_index = marker_indices[\n      0\n    ]\n    consumer_index = consumer_indices[\n      0\n    ]\n\n    if consumer_index <= marker_index:\n      continue\n\n    lines[\n      marker_index\n    ] = (\n      marker\n      + "より、"\n      + consumer_line\n    )\n    del lines[\n      consumer_index\n    ]\n\n  compacted_lines = []\n  previous_blank = False\n\n  for line in lines:\n    is_blank = not line.strip()\n\n    if is_blank and previous_blank:\n      continue\n\n    compacted_lines.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted_lines\n  ).strip()\n'


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  marker = (
    "def "
    + name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + name
    )

  next_def = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_def < 0:
    return (
      source[
        :start
      ]
      + replacement.rstrip()
      + "\n"
    )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      next_def + 1:
    ]
  )


def remove_existing_phase154_r5_helpers(
  source: str,
) -> str:
  names = (
    "_phase154_r5_selected_reference_steps_by_number",
    "_phase154_r5_reference_source_steps_by_number",
    "_phase154_r5_unique_visible_non_root_consumer_line",
    "link_toda_group_proof_narrative_reference_body_consumers",
  )

  updated = source

  for name in names:
    marker = (
      "def "
      + name
      + "("
    )
    start = updated.find(
      marker
    )

    if start < 0:
      continue

    next_def = updated.find(
      "\ndef ",
      start + len(
        marker
      ),
    )

    if next_def < 0:
      updated = updated[
        :start
      ]
      continue

    updated = (
      updated[
        :start
      ]
      + updated[
        next_def + 1:
      ]
    )

  return updated


def insert_before_function(
  source: str,
  name: str,
  addition: str,
) -> str:
  marker = (
    "def "
    + name
    + "("
  )
  index = source.find(
    marker
  )

  if index < 0:
    raise RuntimeError(
      "insertion target not found: "
      + name
    )

  return (
    source[
      :index
    ]
    + addition.rstrip()
    + "\n\n"
    + source[
      index:
    ]
  )


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "missing production file: "
      + str(
        TARGET
      )
    )

  BACKUP.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP,
  )

  source = TARGET.read_text(
    encoding="utf-8",
  )
  source = remove_existing_phase154_r5_helpers(
    source
  )
  source = insert_before_function(
    source,
    "suppress_toda_group_proof_narrative_reference_body_duplicates",
    HELPERS,
  )
  TARGET.write_text(
    source,
    encoding="utf-8",
  )

  test_source = (
    Path(__file__).resolve().parent
    / "tests"
    / "test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py"
  )
  test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py"
  )
  shutil.copy2(
    test_source,
    test_target,
  )

  print(
    "updated:",
    TARGET.name,
  )
  print(
    "added:",
    test_target.relative_to(
      REPO_ROOT
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
