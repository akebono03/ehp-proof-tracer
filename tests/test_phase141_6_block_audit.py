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


def _pi6_3_presentation():
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
      max_depth=3,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase141_6_blocks_cover_selected_graph_exactly_once():
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

  assert len(
    {
      id(
        proof_step
      )
      for proof_step in block_steps
    }
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


def test_phase141_6_every_block_matches_step_role_recognition():
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

  for block in blocks:
    for proof_step in block.steps:
      assert (
        recognize_toda_group_proof_narrative_step_role(
          presentation,
          proof_step,
          semantic_sidecar=sidecar,
        )
        is block.role
      )


def test_phase141_6_pi6_3_has_one_precondition_block():
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

  precondition_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION
    )
  )

  assert len(
    precondition_blocks
  ) == 1

  assert len(
    precondition_blocks[
      0
    ].steps
  ) == 1


def test_phase141_6_pi6_3_has_one_definition_introduction_block():
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

  definition_steps = {
    id(
      semantic.proof_step
    )
    for semantic in (
      sidecar.step_semantics
    )
  }

  definition_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
      and any(
        id(
          proof_step
        )
        in definition_steps
        for proof_step
        in block.steps
      )
    )
  )

  assert len(
    definition_blocks
  ) == 1


def test_phase141_6_pi6_3_contains_core_mathematical_roles():
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

  roles = {
    block.role
    for block in blocks
  }

  assert {
    TodaGroupProofNarrativeMathematicalBlockRole.TARGET,
    TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION,
    TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION,
    TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
    TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION,
    TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
    TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
    TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
    TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
  }.issubset(
    roles
  )


def test_phase141_6_semantic_annotations_are_not_lost_in_other():
  presentation = (
    _pi6_3_presentation()
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  for semantic in (
    sidecar.step_semantics
  ):
    assert (
      recognize_toda_group_proof_narrative_step_role(
        presentation,
        semantic.proof_step,
        semantic_sidecar=sidecar,
      )
      is not TodaGroupProofNarrativeMathematicalBlockRole.OTHER
    )

  for semantic in (
    sidecar.premise_semantics
  ):
    assert (
      recognize_toda_group_proof_narrative_step_role(
        presentation,
        semantic.edge.premise_step,
        semantic_sidecar=sidecar,
      )
      is not TodaGroupProofNarrativeMathematicalBlockRole.OTHER
    )
