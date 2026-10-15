from collections import deque

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)


CASES = (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _build_case(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      closure
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    closure,
    semantic_sidecar=sidecar,
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      closure,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  chains = (
    build_toda_group_proof_narrative_proof_chains(
      closure,
      sidecar,
      arguments,
    )
  )
  contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      closure,
      blocks,
      sidecar,
      arguments,
      chains,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  return (
    closure,
    sidecar,
    blocks,
    arguments,
    chains,
    contributions,
    rendered,
  )


def _step_consumers(
  presentation,
):
  result = {}

  for edge in presentation.edges:
    result.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  return result


def _semantic_consumers(
  sidecar,
):
  result = {}

  for semantic in sidecar.dependency_semantics:
    result.setdefault(
      id(
        semantic.prerequisite_step
      ),
      [],
    ).append(
      semantic.dependent_step
    )

  return result


def _combined_consumers(
  presentation,
  sidecar,
):
  proof_consumers = _step_consumers(
    presentation
  )
  semantic_consumers = _semantic_consumers(
    sidecar
  )
  result = {}

  for step_id in (
    set(
      proof_consumers
    )
    | set(
      semantic_consumers
    )
  ):
    seen = set()
    consumers = []

    for consumer in (
      tuple(
        proof_consumers.get(
          step_id,
          ()
        )
      )
      + tuple(
        semantic_consumers.get(
          step_id,
          ()
        )
      )
    ):
      consumer_id = id(
        consumer
      )
      if consumer_id in seen:
        continue
      seen.add(
        consumer_id
      )
      consumers.append(
        consumer
      )

    result[
      step_id
    ] = tuple(
      consumers
    )

  return result


def _first_argument_handoff_paths(
  source_argument_index,
  source_step,
  arguments,
  conclusion_argument_index_by_step_id,
  consumers,
):
  queue = deque(
    [
      (
        source_step,
        (
          source_step,
        ),
      ),
    ]
  )
  visited = {
    id(
      source_step
    ),
  }
  paths = []

  while queue:
    current_step, path = queue.popleft()

    for consumer in consumers.get(
      id(
        current_step
      ),
      (),
    ):
      consumer_id = id(
        consumer
      )
      consumer_argument_index = (
        conclusion_argument_index_by_step_id.get(
          consumer_id
        )
      )

      next_path = (
        path
        + (
          consumer,
        )
      )

      if (
        consumer_argument_index is not None
        and consumer_argument_index
        != source_argument_index
      ):
        paths.append(
          (
            consumer_argument_index,
            next_path,
          )
        )
        continue

      if consumer_id in visited:
        continue

      visited.add(
        consumer_id
      )
      queue.append(
        (
          consumer,
          next_path,
        )
      )

  return tuple(
    paths
  )


def _step_label(
  proof_step,
):
  rendered = _render_generic_narrative_step(
    proof_step
  )
  if rendered:
    return rendered.replace(
      "\n",
      " ",
    )

  return repr(
    proof_step.conclusion
  )


def _block_index_by_step_id(
  blocks,
):
  return {
    id(
      proof_step
    ): block_index
    for block_index, block in enumerate(
      blocks
    )
    for proof_step in block.steps
  }


def audit_case(
  label,
  n,
  k,
):
  (
    presentation,
    sidecar,
    blocks,
    arguments,
    chains,
    contributions,
    rendered,
  ) = _build_case(
    n,
    k,
  )

  conclusion_steps = tuple(
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    for argument in arguments
  )
  conclusion_argument_index_by_step_id = {
    id(
      proof_step
    ): argument_index
    for argument_index, proof_step in enumerate(
      conclusion_steps
    )
    if proof_step is not None
  }
  consumers = _combined_consumers(
    presentation,
    sidecar,
  )
  block_index_by_step_id = (
    _block_index_by_step_id(
      blocks
    )
  )

  print(
    "=" * 110
  )
  print(
    label
  )
  print(
    "=" * 110
  )
  print(
    "presentation_nodes="
    + str(
      len(
        presentation.nodes
      )
    )
  )
  print(
    "arguments="
    + str(
      len(
        arguments
      )
    )
  )
  print()

  implicit_handoff_count = 0
  explicit_handoff_count = 0
  rendered_handoff_count = 0

  for argument_index, argument in enumerate(
    arguments
  ):
    conclusion_step = conclusion_steps[
      argument_index
    ]
    purpose = (
      extract_toda_group_proof_narrative_argument_purpose_subject(
        argument
      )
    )
    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    local_block_indices = tuple(
      blocks.index(
        block
      )
      for block in local_body
    )

    print(
      "ARGUMENT A"
      + f"{argument_index:02d}"
    )
    print(
      "  role="
      + argument.role.value
    )
    print(
      "  purpose="
      + repr(
        purpose
      )
    )
    print(
      "  child_argument_indices="
      + repr(
        argument.child_argument_indices
      )
    )
    print(
      "  local_body_block_indices="
      + repr(
        local_block_indices
      )
    )
    print(
      "  contribution_count="
      + str(
        len(
          contributions[
            argument_index
          ]
        )
      )
    )

    if conclusion_step is None:
      print(
        "  conclusion_step=None"
      )
      print()
      continue

    conclusion_line = _step_label(
      conclusion_step
    )
    print(
      "  conclusion="
      + conclusion_line
    )
    print(
      "  conclusion_visible="
      + str(
        conclusion_line in rendered
      )
    )

    handoffs = _first_argument_handoff_paths(
      argument_index,
      conclusion_step,
      arguments,
      conclusion_argument_index_by_step_id,
      consumers,
    )

    if not handoffs:
      print(
        "  HANDOFFS=()"
      )
      print()
      continue

    for handoff_index, (
      target_argument_index,
      path,
    ) in enumerate(
      handoffs
    ):
      target_argument = arguments[
        target_argument_index
      ]
      target_conclusion_step = (
        conclusion_steps[
          target_argument_index
        ]
      )
      intermediate_steps = path[
        1:-1
      ]
      intermediate_block_indices = tuple(
        block_index_by_step_id.get(
          id(
            proof_step
          )
        )
        for proof_step in intermediate_steps
      )
      explicit_child = (
        target_argument_index
        in argument.child_argument_indices
      )
      source_line_visible = (
        conclusion_line in rendered
      )
      target_line = (
        None
        if target_conclusion_step is None
        else _step_label(
          target_conclusion_step
        )
      )
      target_line_visible = (
        False
        if target_line is None
        else target_line in rendered
      )

      if explicit_child:
        explicit_handoff_count += 1
      else:
        implicit_handoff_count += 1

      if (
        source_line_visible
        and target_line_visible
      ):
        rendered_handoff_count += 1

      print(
        "  HANDOFF H"
        + f"{handoff_index:02d}"
      )
      print(
        "    target=A"
        + f"{target_argument_index:02d}"
        + " role="
        + target_argument.role.value
      )
      print(
        "    explicit_child="
        + str(
          explicit_child
        )
      )
      print(
        "    path_length="
        + str(
          len(
            path
          )
        )
      )
      print(
        "    intermediate_block_indices="
        + repr(
          intermediate_block_indices
        )
      )
      print(
        "    source_visible="
        + str(
          source_line_visible
        )
      )
      print(
        "    target_visible="
        + str(
          target_line_visible
        )
      )
      for path_index, proof_step in enumerate(
        path
      ):
        print(
          "      P"
          + f"{path_index:02d}"
          + " B"
          + str(
            block_index_by_step_id.get(
              id(
                proof_step
              )
            )
          )
          + " "
          + _step_label(
            proof_step
          )
        )

    print()

  print(
    "EXPLICIT_HANDOFF_COUNT="
    + str(
      explicit_handoff_count
    )
  )
  print(
    "IMPLICIT_HANDOFF_COUNT="
    + str(
      implicit_handoff_count
    )
  )
  print(
    "BOTH_ENDPOINTS_VISIBLE_HANDOFF_COUNT="
    + str(
      rendered_handoff_count
    )
  )
  print(
    "HAS_IMPLICIT_HANDOFFS="
    + str(
      implicit_handoff_count
      > 0
    )
  )
  print(
    "RENDERED_HAS_GENERIC_GRAPH_CONNECTORS="
    + str(
      (
        "これらから" in rendered
        or "このことから" in rendered
      )
    )
  )
  print(
    "RENDERED_NARRATIVE_BEGIN"
  )
  print(
    rendered
  )
  print(
    "RENDERED_NARRATIVE_END"
  )
  print()

  return (
    implicit_handoff_count
  )


def main():
  print(
    "Phase 150 RC4-7B-2 Intermediate-Conclusion Handoff Audit"
  )
  print(
    "Production changes: none"
  )
  print()

  implicit_total = 0

  for label, n, k in CASES:
    implicit_total += audit_case(
      label,
      n,
      k,
    )

  print(
    "=" * 110
  )
  print(
    "CROSS-GROUP SUMMARY"
  )
  print(
    "=" * 110
  )
  print(
    "IMPLICIT_HANDOFF_TOTAL="
    + str(
      implicit_total
    )
  )
  print(
    "INTERMEDIATE_CONCLUSION_HANDOFF_GAP_DETECTED="
    + str(
      implicit_total
      > 0
    )
  )
  print(
    "AUDIT_DECISION=CLASSIFY_HANDOFF_PATHS_BEFORE_PRODUCTION_CHANGE"
  )


if __name__ == "__main__":
  main()
