from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_classifier import (
  TodaGroupProofNarrativeBlockRole,
  TodaGroupProofNarrativeFactRole,
  classify_toda_group_proof_narrative_step,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation(
  n,
  k,
):
  report = (
    build_standard_toda_report(
      n=n,
      k=k,
    )
  )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def test_phase134_9_pi6_3_root_is_target(
):
  presentation = _presentation(
    3,
    3,
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      presentation.root_step,
    )
  )

  assert (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.TARGET
  )

  assert (
    classification.block_role
    is TodaGroupProofNarrativeBlockRole.GROUP_STRUCTURE
  )


def test_phase134_9_pi6_3_has_reference_boundary_and_derived(
):
  presentation = _presentation(
    3,
    3,
  )

  roles = tuple(
    classify_toda_group_proof_narrative_step(
      presentation,
      node.proof_step,
    ).fact_role
    for node in presentation.nodes
  )

  assert (
    TodaGroupProofNarrativeFactRole.REFERENCE
    in roles
  )

  assert (
    TodaGroupProofNarrativeFactRole.BOUNDARY
    in roles
  )

  assert (
    TodaGroupProofNarrativeFactRole.DERIVED
    in roles
  )


def test_phase134_9_pi8_5_uses_same_four_fact_roles(
):
  presentation = _presentation(
    5,
    3,
  )

  roles = tuple(
    classify_toda_group_proof_narrative_step(
      presentation,
      node.proof_step,
    ).fact_role
    for node in presentation.nodes
  )

  assert (
    TodaGroupProofNarrativeFactRole.TARGET
    in roles
  )

  assert (
    TodaGroupProofNarrativeFactRole.REFERENCE
    in roles
  )

  assert (
    TodaGroupProofNarrativeFactRole.BOUNDARY
    in roles
  )

  assert (
    TodaGroupProofNarrativeFactRole.DERIVED
    in roles
  )


def test_phase134_9_pi8_5_has_order_and_group_structure_blocks(
):
  presentation = _presentation(
    5,
    3,
  )

  block_roles = tuple(
    classify_toda_group_proof_narrative_step(
      presentation,
      node.proof_step,
    ).block_role
    for node in presentation.nodes
  )

  assert (
    TodaGroupProofNarrativeBlockRole.ORDER
    in block_roles
  )

  assert (
    TodaGroupProofNarrativeBlockRole.GROUP_STRUCTURE
    in block_roles
  )
