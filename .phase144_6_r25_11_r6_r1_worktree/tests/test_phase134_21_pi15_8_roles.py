from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_classifier import (
  TodaGroupProofNarrativeBlockRole,
  TodaGroupProofNarrativeFactRole,
  classify_toda_group_proof_narrative_step,
)
from toda_group_proof_narrative_catalog import (
  REFERENCE_CANDIDATE_STATEMENT_TYPES,
  REFERENCE_STATEMENT_TYPES_BY_ROOT,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp44IsomorphismStatement,
)


def _pi15_8_presentation():
  report = build_standard_toda_report(
    n=8,
    k=7,
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

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase134_21_prop44_is_reference_candidate(
):
  assert (
    TodaProp44IsomorphismStatement
    in REFERENCE_CANDIDATE_STATEMENT_TYPES
  )


def test_phase134_21_pi15_8_reference_scope_is_prop44(
):
  assert (
    REFERENCE_STATEMENT_TYPES_BY_ROOT[
      (
        15,
        8,
      )
    ]
    == (
      TodaProp44IsomorphismStatement,
    )
  )


def test_phase134_21_pi15_8_prop44_is_reference(
):
  presentation = (
    _pi15_8_presentation()
  )

  prop44_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp44IsomorphismStatement,
    )
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      prop44_step,
    )
  )

  assert (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.REFERENCE
  )


def test_phase134_21_transported_decomposition_is_derived_group_structure(
):
  presentation = (
    _pi15_8_presentation()
  )

  transported_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      Toda515Sigma8TransportedDecompositionStatement,
    )
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      transported_step,
    )
  )

  assert (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.DERIVED
  )

  assert (
    classification.block_role
    is TodaGroupProofNarrativeBlockRole.GROUP_STRUCTURE
  )
