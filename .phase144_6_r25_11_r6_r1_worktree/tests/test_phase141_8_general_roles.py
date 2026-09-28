from homotopy_groups import (
  TodaPrimaryGroupZeroStatement,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
  recognize_toda_group_proof_narrative_step_role,
)
from toda_group_proof_narrative_catalog import (
  REFERENCE_STATEMENT_TYPES,
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
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  TodaDeltaImageUpToSignStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
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


def _role_by_statement_type(
  presentation,
  sidecar,
  statement_type,
):
  step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      statement_type,
    )
  )

  return (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      step,
      semantic_sidecar=sidecar,
    )
  )


def test_phase141_8_reference_catalog_contains_general_reference_types():
  assert {
    Toda52CompositionIsomorphismStatement,
    Toda53NuPrimeBracketSpecializationStatement,
    TodaProp44IsomorphismStatement,
    TodaProp44SecondSummandRestrictionStatement,
    TodaProp51FiniteDimensionalStatement,
  }.issubset(
    set(
      REFERENCE_STATEMENT_TYPES
    )
  )


def test_phase141_8_pi6_3_known_reference_steps_are_reference_blocks():
  presentation = (
    _pi6_3_presentation()
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  for statement_type in (
    Toda52CompositionIsomorphismStatement,
    Toda53NuPrimeBracketSpecializationStatement,
    TodaProp44IsomorphismStatement,
    TodaProp44SecondSummandRestrictionStatement,
    TodaProp51FiniteDimensionalStatement,
  ):
    assert (
      _role_by_statement_type(
        presentation,
        sidecar,
        statement_type,
      )
      is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE
    )


def test_phase141_8_pi6_3_delta_image_is_map_property():
  presentation = (
    _pi6_3_presentation()
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  assert (
    _role_by_statement_type(
      presentation,
      sidecar,
      TodaDeltaImageUpToSignStatement,
    )
    is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
  )


def test_phase141_8_pi6_3_zero_group_is_group_structure():
  presentation = (
    _pi6_3_presentation()
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  assert (
    _role_by_statement_type(
      presentation,
      sidecar,
      TodaPrimaryGroupZeroStatement,
    )
    is TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE
  )


def test_phase141_8_pi6_3_has_no_other_blocks():
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

  assert all(
    block.role
    is not TodaGroupProofNarrativeMathematicalBlockRole.OTHER
    for block in blocks
  )


def test_phase141_8_sidecar_roles_still_take_precedence():
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

  definition_step = (
    sidecar.step_semantics[
      0
    ].proof_step
  )

  assert (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      precondition_step,
      semantic_sidecar=sidecar,
    )
    is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION
  )

  assert (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      definition_step,
      semantic_sidecar=sidecar,
    )
    is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
  )
