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
  extract_toda_group_proof_narrative_argument_conclusion_step,
)


def _pi6_3_context():
  return _method_evidence_data(
    3,
    3,
  )


def _argument_index(
  arguments,
  role,
):
  return next(
    index
    for index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )


def test_phase144_6_r25_9a_order_does_not_protect_second_level_premises():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _pi6_3_context()

  argument_index = _argument_index(
    arguments,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )
  argument = arguments[
    argument_index
  ]
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
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
  hidden = (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      sidecar,
      argument,
    )
  )

  second_level_ids = {
    id(
      support_step
    )
    for premise_step in conclusion_step.premises
    for support_step in premise_step.premises
  }

  assert second_level_ids
  assert any(
    step_id in hidden
    for step_id in second_level_ids
  )


def test_phase144_6_r25_9a_definition_keeps_second_level_frontier():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _pi6_3_context()

  argument_index = _argument_index(
    arguments,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )
  argument = arguments[
    argument_index
  ]
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
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
  hidden = (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      sidecar,
      argument,
    )
  )

  direct_premise_steps = list(
    conclusion_step.premises
  )
  direct_premise_steps.extend(
    semantic.prerequisite_step
    for semantic in sidecar.dependency_semantics
    if semantic.dependent_step is conclusion_step
  )
  second_level_ids = {
    id(
      support_step
    )
    for premise_step in direct_premise_steps
    for support_step in premise_step.premises
  }

  assert second_level_ids
  assert all(
    step_id not in hidden
    for step_id in second_level_ids
  )


def test_phase144_6_r25_9a_pi5_3_is_hidden_without_losing_transitions():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _pi6_3_context()

  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  assert (
    r"\pi_{5}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\eta_{4}\}"
    not in rendered
  )
  assert r"$\nu'$ を定める." in rendered
  assert r"2\nu' = \eta_{3}^{3}" in rendered
  assert "(1) と (2) より、" in rendered
  assert r"H\left(\nu'\right) = \eta_{5}" in rendered
  assert "(4) と (5) より、" in rendered
  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in rendered
  )
