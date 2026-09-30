from collections import Counter

from audit_phase150_rc4_7b_2_support import (
  CASES,
  _block_index_by_step_id,
  _build_case,
  _combined_consumers,
  _first_argument_handoff_paths,
  _step_label,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_transitions import (
  extract_toda_group_proof_narrative_transitions,
)


def _local_body_step_ids_by_argument(
  presentation,
  blocks,
  sidecar,
  arguments,
):
  result = []

  for argument_index in range(len(arguments)):
    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    result.append(
      frozenset(
        id(proof_step)
        for block in local_body
        for proof_step in block.steps
      )
    )

  return tuple(result)


def _classify_handoff(
  source_visible,
  target_visible,
  path,
  target_local_body_step_ids,
):
  intermediate_steps = path[1:-1]

  if not source_visible or not target_visible:
    return "HIDDEN_ENDPOINT"

  if len(path) == 2:
    return "DIRECT_ARGUMENT_HANDOFF"

  if all(
    id(proof_step) in target_local_body_step_ids
    for proof_step in intermediate_steps
  ):
    return "TARGET_LOCAL_DERIVATION_HANDOFF"

  return "TRANSITIVE_EXTERNAL_DEPENDENCY"


def _transition_role_by_target_block_id(
  transitions,
):
  return {
    id(transition.target_block): transition.role.value
    for transition in transitions
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

  transitions = (
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    )
  )
  transition_role_by_target_block_id = (
    _transition_role_by_target_block_id(
      transitions
    )
  )

  conclusion_steps = tuple(
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    for argument in arguments
  )
  conclusion_argument_index_by_step_id = {
    id(proof_step): argument_index
    for argument_index, proof_step in enumerate(conclusion_steps)
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
  local_body_step_ids = (
    _local_body_step_ids_by_argument(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  counts = Counter()
  candidates = []

  print("=" * 110)
  print(label)
  print("=" * 110)
  print("presentation_nodes=" + str(len(presentation.nodes)))
  print("arguments=" + str(len(arguments)))
  print()

  for source_argument_index, source_argument in enumerate(arguments):
    source_step = conclusion_steps[source_argument_index]
    if source_step is None:
      continue

    source_line = _step_label(source_step)
    source_visible = source_line in rendered

    handoffs = _first_argument_handoff_paths(
      source_argument_index,
      source_step,
      arguments,
      conclusion_argument_index_by_step_id,
      consumers,
    )

    for handoff_index, (
      target_argument_index,
      path,
    ) in enumerate(handoffs):
      target_argument = arguments[target_argument_index]
      target_step = conclusion_steps[target_argument_index]
      if target_step is None:
        continue

      target_line = _step_label(target_step)
      target_visible = target_line in rendered
      classification = _classify_handoff(
        source_visible,
        target_visible,
        path,
        local_body_step_ids[target_argument_index],
      )
      counts[classification] += 1

      intermediate_steps = path[1:-1]
      intermediate_block_indices = tuple(
        block_index_by_step_id.get(id(proof_step))
        for proof_step in intermediate_steps
      )
      target_local_flags = tuple(
        id(proof_step) in local_body_step_ids[target_argument_index]
        for proof_step in intermediate_steps
      )
      transition_role = (
        transition_role_by_target_block_id.get(
          id(target_argument.conclusion_block),
          "NONE",
        )
      )

      if classification in (
        "DIRECT_ARGUMENT_HANDOFF",
        "TARGET_LOCAL_DERIVATION_HANDOFF",
      ):
        candidates.append(
          (
            source_argument_index,
            target_argument_index,
            classification,
            path,
          )
        )

      print(
        "HANDOFF "
        + label
        + " A"
        + f"{source_argument_index:02d}"
        + "->A"
        + f"{target_argument_index:02d}"
        + " H"
        + f"{handoff_index:02d}"
      )
      print("  CLASS=" + classification)
      print("  source_role=" + source_argument.role.value)
      print("  target_role=" + target_argument.role.value)
      print("  target_transition_role=" + transition_role)
      print(
        "  explicit_child="
        + str(
          target_argument_index
          in source_argument.child_argument_indices
        )
      )
      print("  source_visible=" + str(source_visible))
      print("  target_visible=" + str(target_visible))
      print("  path_length=" + str(len(path)))
      print(
        "  intermediate_block_indices="
        + repr(intermediate_block_indices)
      )
      print(
        "  intermediate_in_target_local_body="
        + repr(target_local_flags)
      )
      print("  source=" + source_line)
      print("  target=" + target_line)

      for path_index, proof_step in enumerate(path):
        print(
          "    P"
          + f"{path_index:02d}"
          + " B"
          + str(
            block_index_by_step_id.get(
              id(proof_step)
            )
          )
          + " "
          + _step_label(proof_step)
        )
      print()

  print(
    "CASE_CLASSIFICATION_COUNTS="
    + repr(dict(sorted(counts.items())))
  )
  print(
    "CASE_CANDIDATE_HANDOFF_COUNT="
    + str(len(candidates))
  )
  print(
    "CASE_TRANSITIVE_EXTERNAL_COUNT="
    + str(
      counts["TRANSITIVE_EXTERNAL_DEPENDENCY"]
    )
  )
  print(
    "CASE_HIDDEN_ENDPOINT_COUNT="
    + str(
      counts["HIDDEN_ENDPOINT"]
    )
  )
  print(
    "RENDERED_HAS_GENERIC_GRAPH_CONNECTORS="
    + str(
      "これらから" in rendered
      or "このことから" in rendered
    )
  )
  print()

  print("CANDIDATE_HANDOFFS_BEGIN")
  if not candidates:
    print("  NONE")

  for (
    source_argument_index,
    target_argument_index,
    classification,
    path,
  ) in candidates:
    source_argument = arguments[source_argument_index]
    target_argument = arguments[target_argument_index]
    print(
      "  A"
      + f"{source_argument_index:02d}"
      + " -> A"
      + f"{target_argument_index:02d}"
      + " "
      + classification
    )
    print(
      "    source_purpose="
      + repr(
        extract_toda_group_proof_narrative_argument_purpose_subject(
          source_argument
        )
      )
    )
    print(
      "    target_purpose="
      + repr(
        extract_toda_group_proof_narrative_argument_purpose_subject(
          target_argument
        )
      )
    )
    print(
      "    source_conclusion="
      + _step_label(path[0])
    )
    print(
      "    target_conclusion="
      + _step_label(path[-1])
    )

  print("CANDIDATE_HANDOFFS_END")
  print()
  print("RENDERED_NARRATIVE_BEGIN")
  print(rendered)
  print("RENDERED_NARRATIVE_END")
  print()

  return counts


def main():
  print(
    "Phase 150 RC4-7B-3 Handoff Classification Audit"
  )
  print("Production changes: none")
  print(
    "Classification only; no child_argument_indices repair."
  )
  print()

  total_counts = Counter()

  for label, n, k in CASES:
    total_counts.update(
      audit_case(
        label,
        n,
        k,
      )
    )

  candidate_total = (
    total_counts["DIRECT_ARGUMENT_HANDOFF"]
    + total_counts[
      "TARGET_LOCAL_DERIVATION_HANDOFF"
    ]
  )

  print("=" * 110)
  print("CROSS-GROUP SUMMARY")
  print("=" * 110)
  print(
    "CLASSIFICATION_COUNTS="
    + repr(dict(sorted(total_counts.items())))
  )
  print(
    "CANDIDATE_HANDOFF_TOTAL="
    + str(candidate_total)
  )
  print(
    "TRANSITIVE_EXTERNAL_TOTAL="
    + str(
      total_counts[
        "TRANSITIVE_EXTERNAL_DEPENDENCY"
      ]
    )
  )
  print(
    "HIDDEN_ENDPOINT_TOTAL="
    + str(
      total_counts["HIDDEN_ENDPOINT"]
    )
  )
  print(
    "AUDIT_DECISION="
    "REVIEW_CANDIDATE_HANDOFFS_BEFORE_PRODUCTION_CHANGE"
  )


if __name__ == "__main__":
  main()
