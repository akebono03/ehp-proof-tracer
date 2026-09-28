from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
  recognize_toda_group_proof_narrative_step_role,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


def _pi6_3_presentation(
  max_depth=3,
):
  report = build_standard_toda_report(
    n=3,
    k=3,
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


def test_phase141_5_sidecar_reclassifies_zero_precondition():
  presentation = (
    _pi6_3_presentation()
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  precondition_step = (
    sidecar.premise_semantics[
      0
    ].edge.premise_step
  )

  without_sidecar = (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      precondition_step,
    )
  )
  with_sidecar = (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      precondition_step,
      semantic_sidecar=sidecar,
    )
  )

  assert (
    without_sidecar
    is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
  )
  assert (
    with_sidecar
    is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION
  )


def test_phase141_5_sidecar_reclassifies_definition_introduction():
  presentation = (
    _pi6_3_presentation()
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  definition_step = (
    sidecar.step_semantics[
      0
    ].proof_step
  )

  assert isinstance(
    definition_step.conclusion,
    TodaBracketMembershipStatement,
  )

  without_sidecar = (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      definition_step,
    )
  )
  with_sidecar = (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      definition_step,
      semantic_sidecar=sidecar,
    )
  )

  assert (
    without_sidecar
    is TodaGroupProofNarrativeMathematicalBlockRole.OTHER
  )
  assert (
    with_sidecar
    is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
  )


def test_phase141_5_block_builder_contains_precondition_block():
  presentation = (
    _pi6_3_presentation()
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )

  precondition_step = (
    sidecar.premise_semantics[
      0
    ].edge.premise_step
  )

  matching_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION
      and precondition_step
      in block.steps
    )
  )

  assert len(
    matching_blocks
  ) == 1


def test_phase141_5_block_builder_contains_definition_block():
  presentation = (
    _pi6_3_presentation()
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )

  definition_step = (
    sidecar.step_semantics[
      0
    ].proof_step
  )

  matching_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
      and definition_step
      in block.steps
    )
  )

  assert len(
    matching_blocks
  ) == 1


def test_phase141_5_sidecar_preserves_full_block_coverage():
  presentation = (
    _pi6_3_presentation()
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )

  block_steps = tuple(
    proof_step
    for block in blocks
    for proof_step in block.steps
  )

  assert len(
    block_steps
  ) == len(
    presentation.nodes
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


def test_phase141_5_builder_without_sidecar_preserves_phase141_1_behavior():
  presentation = (
    _pi6_3_presentation()
  )

  first = (
    build_toda_group_proof_narrative_blocks(
      presentation
    )
  )
  second = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=None,
    )
  )

  assert tuple(
    (
      block.role,
      tuple(
        id(
          proof_step
        )
        for proof_step in block.steps
      ),
    )
    for block in first
  ) == tuple(
    (
      block.role,
      tuple(
        id(
          proof_step
        )
        for proof_step in block.steps
      ),
    )
    for block in second
  )
