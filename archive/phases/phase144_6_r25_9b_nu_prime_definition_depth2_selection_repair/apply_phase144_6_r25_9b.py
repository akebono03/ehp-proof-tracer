from pathlib import Path


SEMANTICS = Path(
  "toda_group_proof_narrative_semantics.py"
)
RENDERER = Path(
  "toda_group_proof_narrative_renderer.py"
)


def replace_once(
  path: Path,
  old: str,
  new: str,
) -> None:
  text = path.read_text(
    encoding="utf-8-sig"
  )

  if new in text:
    print(
      f"{path}: target change already applied"
    )
    return

  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{path}: expected exactly one replacement "
      f"anchor, found {count}"
    )

  path.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )

  print(
    f"updated {path}"
  )


replace_once(
  SEMANTICS,
  """from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_dependency import (
  TodaProofEdge,
)
""",
  """from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  TodaGroupResultProofReplayResult,
  TodaGroupResultProofReplayStep,
)
from toda_proof_dependency import (
  TodaProofEdge,
  extract_toda_recursive_proof_provenance,
)
""",
)

replace_once(
  SEMANTICS,
  """def _semantic_dependency_semantics(
""",
  """def build_toda_group_proof_narrative_semantic_closure_presentation(
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


def _semantic_dependency_semantics(
""",
)

replace_once(
  RENDERER,
  """from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
""",
  """from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
""",
)

replace_once(
  RENDERER,
  """  phase134_24_pi15_8 = (
""",
  """  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  phase134_24_pi15_8 = (
""",
)

print(
  "R25-9B semantic closure selection repair applied."
)
