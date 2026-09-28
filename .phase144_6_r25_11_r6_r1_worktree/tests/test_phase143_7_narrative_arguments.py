import inspect

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
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


def _presentation(
  n,
  k,
  max_depth=3,
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


def _arguments(
  n,
  k,
):
  presentation = _presentation(
    n,
    k,
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )


def test_phase143_7_pi6_3_builds_minimal_argument_roles():
  _, _, _, arguments = _arguments(
    3,
    3,
  )

  roles = {
    argument.role
    for argument in arguments
  }

  assert (
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
    in roles
  )
  assert (
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    in roles
  )
  assert (
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    in roles
  )


def test_phase143_7_definition_argument_contains_precondition():
  _, _, _, arguments = _arguments(
    3,
    3,
  )

  definition_argument = next(
    argument
    for argument in arguments
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
    )
  )

  assert (
    definition_argument.conclusion_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
  )
  assert any(
    block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION
    for block in definition_argument.supporting_blocks
  )


def test_phase143_7_order_argument_uses_dependency_closure():
  _, _, _, arguments = _arguments(
    3,
    3,
  )

  order_argument = next(
    argument
    for argument in arguments
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    )
  )

  assert (
    order_argument.conclusion_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.ORDER
  )
  assert order_argument.supporting_blocks
  assert all(
    block is not order_argument.conclusion_block
    for block in order_argument.supporting_blocks
  )


def test_phase143_7_target_argument_is_group_structure_argument():
  _, _, _, arguments = _arguments(
    3,
    3,
  )

  target_argument = next(
    argument
    for argument in arguments
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    )
  )

  assert (
    target_argument.conclusion_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
  )
  order_argument_index = next(
    argument_index
    for argument_index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    )
  )

  assert (
    order_argument_index
    in target_argument.child_argument_indices
  )


def test_phase143_7_argument_model_rejects_conclusion_as_support():
  _, _, blocks, _ = _arguments(
    3,
    3,
  )

  target_block = next(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    )
  )

  try:
    TodaGroupProofNarrativeArgument(
      role=(
        TodaGroupProofNarrativeArgumentRole
        .ESTABLISH_GROUP_STRUCTURE
      ),
      supporting_blocks=(
        target_block,
      ),
      conclusion_block=target_block,
    )
  except ValueError:
    pass
  else:
    raise AssertionError(
      "conclusion block must not be accepted as support"
    )


def test_phase143_7_other_group_proofs_build_without_target_specific_rules():
  for n, k in (
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    _, _, _, arguments = _arguments(
      n,
      k,
    )

    assert arguments
    assert any(
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
      for argument in arguments
    )


def test_phase143_7_builder_has_no_pi6_specific_hardcoding():
  source = inspect.getsource(
    build_toda_group_proof_narrative_arguments
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
