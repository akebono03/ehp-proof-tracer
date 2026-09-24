from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_classifier import (
  TodaGroupProofNarrativeFactRole,
  classify_toda_group_proof_narrative_step,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaNuFamilyDefinitionStatement,
)


def _presentation(
  n,
  k,
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
      max_depth=2,
    )
  )

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def test_phase134_11_pi8_5_definition_has_definition_role(
):
  presentation = _presentation(
    5,
    3,
  )

  definition_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaNuFamilyDefinitionStatement,
    )
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      definition_step,
    )
  )

  assert (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.DEFINITION
  )


def test_phase134_11_pi8_5_completed_pi6_3_is_boundary(
):
  presentation = _presentation(
    5,
    3,
  )

  pi6_3_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      hasattr(
        node.proof_step.conclusion,
        "lhs",
      )
      and getattr(
        node.proof_step.conclusion.lhs,
        "group_dimension",
        None,
      )
      == 6
      and getattr(
        node.proof_step.conclusion.lhs,
        "sphere_dimension",
        None,
      )
      == 3
    )
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      pi6_3_step,
    )
  )

  assert (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.BOUNDARY
  )
