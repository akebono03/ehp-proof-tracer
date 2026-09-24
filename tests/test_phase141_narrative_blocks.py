from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
  recognize_toda_group_proof_narrative_step_role,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)


def _presentation(
  n,
  k,
  max_depth=2,
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
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase141_pi6_3_root_is_target_without_target_specific_rule():
  presentation = _presentation(
    3,
    3,
  )

  role = (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      presentation.root_step,
    )
  )

  assert (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
  )


def test_phase141_pi8_5_root_uses_same_target_rule():
  presentation = _presentation(
    5,
    3,
  )

  role = (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      presentation.root_step,
    )
  )

  assert (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
  )


def test_phase141_pi6_3_exactness_is_recognized_from_statement_semantics():
  presentation = _presentation(
    3,
    3,
  )

  exactness_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  role = (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      exactness_step,
    )
  )

  assert (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
  )


def test_phase141_pi6_3_map_properties_are_recognized_from_statement_semantics():
  presentation = _presentation(
    3,
    3,
  )

  map_property_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      (
        TodaSuspensionInjectiveStatement,
        TodaHopfInvariantSurjectiveStatement,
      ),
    )
  )

  assert map_property_steps

  assert all(
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      proof_step,
    )
    is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
    for proof_step in map_property_steps
  )


def test_phase141_pi6_3_order_is_recognized_from_relation_semantics():
  presentation = _presentation(
    3,
    3,
  )

  order_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        Relation,
      )
      and node.proof_step.conclusion.relation_type
      is RelationType.ORDER
    )
  )

  role = (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      order_step,
    )
  )

  assert (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole.ORDER
  )


def test_phase141_block_builder_covers_selected_graph_steps_once_without_mutation():
  presentation = _presentation(
    3,
    3,
  )

  before_nodes = presentation.nodes
  before_edges = presentation.edges

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation
    )
  )

  block_steps = tuple(
    proof_step
    for block in blocks
    for proof_step in block.steps
  )

  assert {
    id(
      proof_step
    )
    for proof_step in block_steps
  } == {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }

  assert len(
    block_steps
  ) == len(
    presentation.nodes
  )

  assert presentation.nodes is before_nodes
  assert presentation.edges is before_edges
