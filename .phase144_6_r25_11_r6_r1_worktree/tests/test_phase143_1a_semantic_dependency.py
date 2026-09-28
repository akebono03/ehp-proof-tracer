from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativePremiseSemanticRole,
  TodaGroupProofNarrativeStepSemanticRole,
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


def test_phase143_1a_sidecar_connects_precondition_to_definition():
  presentation = (
    _pi6_3_presentation()
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  dependencies = (
    sidecar.dependency_semantics
  )

  assert len(
    dependencies
  ) == 1

  dependency = dependencies[
    0
  ]

  assert (
    dependency.role
    is TodaGroupProofNarrativeDependencySemanticRole
    .PRECONDITION_FOR_DEFINITION
  )

  precondition_steps = {
    id(
      semantic.edge.premise_step
    )
    for semantic in sidecar.premise_semantics
    if (
      semantic.role
      is TodaGroupProofNarrativePremiseSemanticRole
      .PRECONDITION
    )
  }
  definition_steps = {
    id(
      semantic.proof_step
    )
    for semantic in sidecar.step_semantics
    if (
      semantic.role
      is TodaGroupProofNarrativeStepSemanticRole
      .DEFINITION_INTRODUCTION
    )
  }

  assert id(
    dependency.prerequisite_step
  ) in precondition_steps
  assert id(
    dependency.dependent_step
  ) in definition_steps


def test_phase143_1a_semantic_dependency_is_not_a_presentation_edge():
  presentation = (
    _pi6_3_presentation()
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  dependency = (
    sidecar.dependency_semantics[
      0
    ]
  )

  assert not any(
    (
      edge.parent_step
      is dependency.dependent_step
      and edge.premise_step
      is dependency.prerequisite_step
    )
    for edge in presentation.edges
  )


def test_phase143_1a_sidecar_build_is_deterministic():
  presentation = (
    _pi6_3_presentation()
  )

  first = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  second = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  assert tuple(
    (
      id(
        semantic.prerequisite_step
      ),
      id(
        semantic.dependent_step
      ),
      semantic.role,
    )
    for semantic in first.dependency_semantics
  ) == tuple(
    (
      id(
        semantic.prerequisite_step
      ),
      id(
        semantic.dependent_step
      ),
      semantic.role,
    )
    for semantic in second.dependency_semantics
  )
