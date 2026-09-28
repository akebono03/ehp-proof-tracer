from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)


PI5_3_TEXT = (
  r"\pi_{5}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\eta_{4}\}"
)


def test_phase144_6_r25_9a_r1_hidden_pi5_3_stays_hidden_after_relocation():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  order_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_ORDER
    )
  )
  order_argument = arguments[
    order_index
  ]
  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      order_index,
    )
  )
  hidden_step_ids = (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      sidecar,
      order_argument,
    )
  )

  pi5_3_steps = tuple(
    proof_step
    for block in local_body
    for proof_step in block.steps
    if (
      PI5_3_TEXT
      in str(
        proof_step.conclusion
      )
      or (
        r"\pi_{5}^{3}"
        in str(
          proof_step.conclusion
        )
        and r"\eta_{3}"
        in str(
          proof_step.conclusion
        )
      )
    )
  )

  assert pi5_3_steps
  assert all(
    id(
      proof_step
    )
    in hidden_step_ids
    for proof_step in pi5_3_steps
  )

  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  assert PI5_3_TEXT not in rendered
