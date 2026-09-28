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
  Toda52CompositionIsomorphismStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaProp51FiniteDimensionalStatement,
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

  return build_toda_group_proof_presentation(
    replay
  )


def _roles_by_statement_type(
  presentation,
):
  result = {}

  for node in presentation.nodes:
    result[
      type(
        node.proof_step.conclusion
      )
    ] = (
      classify_toda_group_proof_narrative_step(
        presentation,
        node.proof_step,
      ).fact_role
    )

  return result


def test_phase134_16_pi6_3_reference_classification_is_unchanged(
):
  roles = _roles_by_statement_type(
    _presentation(
      3,
      3,
    )
  )

  assert roles[
    Toda52CompositionIsomorphismStatement
  ] is TodaGroupProofNarrativeFactRole.REFERENCE

  assert roles[
    TodaProp51FiniteDimensionalStatement
  ] is TodaGroupProofNarrativeFactRole.REFERENCE


def test_phase134_16_pi8_5_reference_classification_is_unchanged(
):
  presentation = _presentation(
    5,
    3,
  )

  seen_reference_types = set()

  for node in presentation.nodes:
    statement = node.proof_step.conclusion

    if isinstance(
      statement,
      (
        Toda55NuFamilyFiniteDimensionalStatement,
        Toda56Nu4DecompositionStatement,
      ),
    ):
      classification = (
        classify_toda_group_proof_narrative_step(
          presentation,
          node.proof_step,
        )
      )

      assert (
        classification.fact_role
        is TodaGroupProofNarrativeFactRole.REFERENCE
      )

      seen_reference_types.add(
        type(
          statement
        )
      )

  assert seen_reference_types.issubset(
    {
      Toda55NuFamilyFiniteDimensionalStatement,
      Toda56Nu4DecompositionStatement,
    }
  )
