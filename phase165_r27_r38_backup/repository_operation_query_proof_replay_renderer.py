from repository_operation_query_proof_replay_presentation import (
  RepositoryOperationQueryProofReplayPresentation,
)
from repository_operation_query_proof_replay_statement_presentation import (
  build_repository_operation_query_proof_replay_statement_presentation,
)


def _render_operation_query_proof_replay_statement(
  statement,
) -> str:
  presentation = (
    build_repository_operation_query_proof_replay_statement_presentation(
      statement
    )
  )

  if presentation.latex is not None:
    return (
      "$"
      + presentation.latex
      + "$"
    )

  return (
    "`"
    + presentation.fallback_type_name
    + "`"
  )


def _operation_query_proof_replay_rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return proof_step.rule.value


def render_repository_operation_query_proof_replay_markdown(
  presentation: RepositoryOperationQueryProofReplayPresentation,
) -> str:
  if not isinstance(
    presentation,
    RepositoryOperationQueryProofReplayPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryOperationQueryProofReplayPresentation"
    )

  source_match = (
    presentation
    .source_result
    .source_match
  )

  node = (
    source_match
    .scope_node
  )

  lines = [
    "# Query fact",
    "",
    "$"
    + presentation.conclusion_latex
    + "$",
    "",
  ]

  theorem = (
    node.root_entry.theorem
  )

  phase = (
    node.root_entry.phase
  )

  if theorem is not None:
    provenance = theorem

    if phase is not None:
      provenance += (
        ", Phase "
        + phase
      )

    provenance += (
      ", depth "
      + str(
        node.shortest_depth
      )
    )
  else:
    provenance = (
      node.root_entry.key
      + ", depth "
      + str(
        node.shortest_depth
      )
    )

  lines.extend(
    (
      "First provenance: "
      + provenance,
      "",
      "## Proof",
      "",
    )
  )

  for index, replay_step in enumerate(
    presentation.steps,
    start=1,
  ):
    proof_step = (
      replay_step.proof_step
    )

    lines.extend(
      (
        (
          str(
            index
          )
          + ". Depth "
          + str(
            replay_step.depth
          )
          + ": "
          + _render_operation_query_proof_replay_statement(
            proof_step.conclusion
          )
        ),
        (
          "   Rule: "
          + _operation_query_proof_replay_rule_name(
            proof_step
          )
        ),
      )
    )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )
