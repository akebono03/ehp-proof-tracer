from pathlib import Path


TARGET = Path(
  "toda_group_proof_narrative_semantics.py"
)
SNAPSHOT_DIR = Path(
  "phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure"
)


OLD_IMPORT = """from proof import (
  ProofStep,
)
"""

NEW_IMPORT = """from proof import (
  ProofStep,
  Relation,
  RelationType,
)
"""


OLD_FUNCTION = """def build_toda_group_proof_narrative_semantic_closure_presentation(
  presentation: TodaGroupProofPresentation,
) -> TodaGroupProofPresentation:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  provenance = (
    extract_toda_recursive_proof_provenance(
      presentation.source_replay.group_result
    )
  )
  selected_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  original_step_ids = frozenset(
    selected_step_ids
  )

  changed = True

  while changed:
    changed = False

    for edge in provenance.edges:
      if (
        id(
          edge.parent_step
        )
        not in selected_step_ids
      ):
        continue

      key = (
        _inference_rule_name(
          edge.parent_step
        ),
        edge.premise_index,
      )

      if (
        key
        not in _STEP_ROLE_BY_CONSUMER_RULE_NAME_AND_INDEX
      ):
        continue

      premise_step_id = id(
        edge.premise_step
      )

      if premise_step_id in selected_step_ids:
        continue

      selected_step_ids.add(
        premise_step_id
      )
      changed = True

  if selected_step_ids == original_step_ids:
    return presentation

  replay_step_by_proof_step_id = {
    id(
      replay_step.proof_step
    ): replay_step
    for replay_step in presentation.source_replay.steps
  }

  for node in provenance.nodes:
    proof_step_id = id(
      node.proof_step
    )

    if (
      proof_step_id not in selected_step_ids
      or proof_step_id
      in replay_step_by_proof_step_id
    ):
      continue

    replay_step_by_proof_step_id[
      proof_step_id
    ] = TodaGroupResultProofReplayStep(
      depth=node.shortest_depth,
      proof_step=node.proof_step,
      role=node.role,
    )

  ordered_steps = tuple(
    replay_step_by_proof_step_id[
      id(
        node.proof_step
      )
    ]
    for node in provenance.nodes
    if (
      id(
        node.proof_step
      )
      in selected_step_ids
    )
  )
  closure_max_depth = max(
    replay_step.depth
    for replay_step in ordered_steps
  )
  source_replay = presentation.source_replay
  closure_replay = (
    TodaGroupResultProofReplayResult(
      group_result=source_replay.group_result,
      source_entry=source_replay.source_entry,
      root_step=source_replay.root_step,
      steps=ordered_steps,
      max_depth=closure_max_depth,
    )
  )

  return build_toda_group_proof_presentation(
    closure_replay
  )
"""

NEW_FUNCTION = """def build_toda_group_proof_narrative_semantic_closure_presentation(
  presentation: TodaGroupProofPresentation,
) -> TodaGroupProofPresentation:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  provenance = (
    extract_toda_recursive_proof_provenance(
      presentation.source_replay.group_result
    )
  )
  selected_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  original_step_ids = frozenset(
    selected_step_ids
  )

  for edge in provenance.edges:
    if (
      id(
        edge.parent_step
      )
      not in original_step_ids
    ):
      continue

    parent_statement = (
      edge.parent_step.conclusion
    )
    premise_statement = (
      edge.premise_step.conclusion
    )

    if (
      not isinstance(
        parent_statement,
        Relation,
      )
      or parent_statement.relation_type
      is not RelationType.EQUALITY
      or not isinstance(
        premise_statement,
        Relation,
      )
      or premise_statement.relation_type
      is not RelationType.EQUALITY
    ):
      continue

    selected_step_ids.add(
      id(
        edge.premise_step
      )
    )

  changed = True

  while changed:
    changed = False

    for edge in provenance.edges:
      if (
        id(
          edge.parent_step
        )
        not in selected_step_ids
      ):
        continue

      key = (
        _inference_rule_name(
          edge.parent_step
        ),
        edge.premise_index,
      )

      if (
        key
        not in _STEP_ROLE_BY_CONSUMER_RULE_NAME_AND_INDEX
      ):
        continue

      premise_step_id = id(
        edge.premise_step
      )

      if premise_step_id in selected_step_ids:
        continue

      selected_step_ids.add(
        premise_step_id
      )
      changed = True

  if selected_step_ids == original_step_ids:
    return presentation

  replay_step_by_proof_step_id = {
    id(
      replay_step.proof_step
    ): replay_step
    for replay_step in presentation.source_replay.steps
  }

  for node in provenance.nodes:
    proof_step_id = id(
      node.proof_step
    )

    if (
      proof_step_id not in selected_step_ids
      or proof_step_id
      in replay_step_by_proof_step_id
    ):
      continue

    replay_step_by_proof_step_id[
      proof_step_id
    ] = TodaGroupResultProofReplayStep(
      depth=node.shortest_depth,
      proof_step=node.proof_step,
      role=node.role,
    )

  ordered_steps = tuple(
    replay_step_by_proof_step_id[
      id(
        node.proof_step
      )
    ]
    for node in provenance.nodes
    if (
      id(
        node.proof_step
      )
      in selected_step_ids
    )
  )
  closure_max_depth = max(
    replay_step.depth
    for replay_step in ordered_steps
  )
  source_replay = presentation.source_replay
  closure_replay = (
    TodaGroupResultProofReplayResult(
      group_result=source_replay.group_result,
      source_entry=source_replay.source_entry,
      root_step=source_replay.root_step,
      steps=ordered_steps,
      max_depth=closure_max_depth,
    )
  )

  return build_toda_group_proof_presentation(
    closure_replay
  )
"""


def _extract_import_snapshot(
  text: str,
) -> str:
  marker = "\n\nclass TodaGroupProofNarrativePremiseSemanticRole"
  index = text.find(
    marker
  )
  if index < 0:
    raise RuntimeError(
      "Could not locate end of import section."
    )
  return text[
    :index
  ].rstrip() + "\n"


def _extract_function_snapshot(
  text: str,
) -> str:
  start_marker = (
    "def build_toda_group_proof_narrative_semantic_closure_presentation(\n"
  )
  end_marker = "\n\ndef _semantic_dependency_semantics("
  start = text.find(
    start_marker
  )
  end = text.find(
    end_marker,
    start,
  )
  if start < 0 or end < 0:
    raise RuntimeError(
      "Could not extract updated closure function."
    )
  return text[
    start:end
  ].rstrip() + "\n"


def main() -> int:
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if NEW_FUNCTION in text:
    print(
      "RC2-4 Repair R4.2 already applied."
    )
  else:
    if text.count(
      OLD_IMPORT
    ) != 1:
      raise RuntimeError(
        "Expected exactly one ProofStep import block."
      )
    if text.count(
      OLD_FUNCTION
    ) != 1:
      raise RuntimeError(
        "Expected exactly one current semantic closure function."
      )

    text = text.replace(
      OLD_IMPORT,
      NEW_IMPORT,
      1,
    )
    text = text.replace(
      OLD_FUNCTION,
      NEW_FUNCTION,
      1,
    )
    TARGET.write_text(
      text,
      encoding="utf-8",
      newline="\n",
    )

  updated = TARGET.read_text(
    encoding="utf-8"
  )
  SNAPSHOT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    SNAPSHOT_DIR
    / "updated_toda_group_proof_narrative_semantics_imports.py.txt"
  ).write_text(
    _extract_import_snapshot(
      updated
    ),
    encoding="utf-8",
    newline="\n",
  )
  (
    SNAPSHOT_DIR
    / "updated_build_toda_group_proof_narrative_semantic_closure_presentation.py.txt"
  ).write_text(
    _extract_function_snapshot(
      updated
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "RC2-4 Repair R4.2 applied."
  )
  print(
    "Changed production file: "
    "toda_group_proof_narrative_semantics.py"
  )
  print(
    "Adds one-level direct equality-premise closure "
    "from steps already selected by the input presentation."
  )
  print(
    "Newly added equality premises are not recursively expanded "
    "by this rule."
  )
  print(
    "Existing registered semantic-definition closure is preserved."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
