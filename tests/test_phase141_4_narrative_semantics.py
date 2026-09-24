from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_semantics import (
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


def test_phase141_4_sidecar_preserves_presentation_identity():
  presentation = (
    _pi6_3_presentation()
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  assert (
    sidecar.presentation
    is presentation
  )


def test_phase141_4_marks_lemma52_second_premises_as_preconditions():
  presentation = (
    _pi6_3_presentation()
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  preconditions = tuple(
    semantic
    for semantic in sidecar.premise_semantics
    if (
      semantic.role
      is TodaGroupProofNarrativePremiseSemanticRole.PRECONDITION
    )
  )

  assert len(
    preconditions
  ) == 3

  assert all(
    semantic.edge.premise_index == 1
    for semantic in preconditions
  )

  assert {
    semantic.edge.parent_step.inference_rule.name
    for semantic in preconditions
  } == {
    (
      "Toda 5.3 nu-prime Lemma 5.2 "
      "Hopf specialization"
    ),
    (
      "Toda 5.3 nu-prime Lemma 5.2 "
      "double specialization"
    ),
    (
      "Toda 5.3 nu-prime Lemma 5.2 "
      "membership specialization"
    ),
  }


def test_phase141_4_precondition_annotations_point_to_existing_zero_relation():
  presentation = (
    _pi6_3_presentation()
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  preconditions = tuple(
    semantic
    for semantic in sidecar.premise_semantics
    if (
      semantic.role
      is TodaGroupProofNarrativePremiseSemanticRole.PRECONDITION
    )
  )

  assert preconditions

  assert all(
    isinstance(
      semantic.edge.premise_step.conclusion,
      Relation,
    )
    and (
      semantic.edge.premise_step.conclusion.relation_type
      is RelationType.ZERO
    )
    for semantic in preconditions
  )

  assert len(
    {
      id(
        semantic.edge.premise_step
      )
      for semantic in preconditions
    }
  ) == 1


def test_phase141_4_marks_bracket_membership_as_definition_introduction():
  presentation = (
    _pi6_3_presentation()
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  definition_introductions = tuple(
    semantic
    for semantic in sidecar.step_semantics
    if (
      semantic.role
      is TodaGroupProofNarrativeStepSemanticRole.DEFINITION_INTRODUCTION
    )
  )

  assert len(
    definition_introductions
  ) == 1

  proof_step = (
    definition_introductions[
      0
    ].proof_step
  )

  assert isinstance(
    proof_step.conclusion,
    TodaBracketMembershipStatement,
  )

  assert (
    proof_step.rule
    is ProofRule.GIVEN
  )


def test_phase141_4_definition_introduction_is_discovered_from_consumer_edge():
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

  incoming_consumer_edges = tuple(
    edge
    for edge in presentation.edges
    if (
      edge.premise_step
      is definition_step
    )
  )

  assert any(
    (
      edge.parent_step.inference_rule
      is not None
      and edge.parent_step.inference_rule.name
      == (
        "Toda 5.3 nu-prime Lemma 5.2 "
        "bracket specialization"
      )
      and edge.premise_index == 0
    )
    for edge in incoming_consumer_edges
  )


def test_phase141_4_sidecar_does_not_mutate_presentation_graph():
  presentation = (
    _pi6_3_presentation()
  )

  before_nodes = presentation.nodes
  before_edges = presentation.edges

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

  assert presentation.nodes is before_nodes
  assert presentation.edges is before_edges

  assert tuple(
    (
      id(
        semantic.edge.parent_step
      ),
      id(
        semantic.edge.premise_step
      ),
      semantic.edge.premise_index,
      semantic.role,
    )
    for semantic in first.premise_semantics
  ) == tuple(
    (
      id(
        semantic.edge.parent_step
      ),
      id(
        semantic.edge.premise_step
      ),
      semantic.edge.premise_index,
      semantic.role,
    )
    for semantic in second.premise_semantics
  )

  assert tuple(
    (
      id(
        semantic.proof_step
      ),
      semantic.role,
    )
    for semantic in first.step_semantics
  ) == tuple(
    (
      id(
        semantic.proof_step
      ),
      semantic.role,
    )
    for semantic in second.step_semantics
  )
