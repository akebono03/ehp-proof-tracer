from expression import (
  Zero,
  eta,
  nu,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_round,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  zero_equality_implies_zero_inference_rule,
)
from stable_rules import (
  SuspensionEpimorphismStatement,
  SuspensionInjectiveStatement,
  SuspensionIsomorphismStatement,
  SuspensionMapEqualityStatement,
  SuspensionMapStatement,
  SuspensionMapZeroStatement,
  freudenthal_boundary_epimorphism_inference_rule,
  freudenthal_stable_isomorphism_inference_rule,
  is_freudenthal_boundary_range,
  is_freudenthal_stable_range,
  suspension_injectivity_reflects_equality_inference_rule,
  suspension_injectivity_reflects_zero_inference_rule,
  suspension_isomorphism_implies_injective_inference_rule,
)


def test_suspension_map_statement():
  statement = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  assert statement.sphere_dimension == 5
  assert statement.stem == 2


def test_suspension_map_statement_has_structural_equality():
  first = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  second = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  assert first == second


def test_suspension_map_statement_distinguishes_source_groups():
  first = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  different_sphere = SuspensionMapStatement(
    sphere_dimension=6,
    stem=2,
  )

  different_stem = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  assert first != different_sphere
  assert first != different_stem


def test_freudenthal_stable_range_includes_boundary_of_isomorphism_range():
  statement = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  assert is_freudenthal_stable_range(
    statement,
  )


def test_freudenthal_stable_range_includes_lower_stems():
  statement = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  assert is_freudenthal_stable_range(
    statement,
  )


def test_freudenthal_boundary_range():
  statement = SuspensionMapStatement(
    sphere_dimension=5,
    stem=4,
  )

  assert not is_freudenthal_stable_range(
    statement,
  )

  assert is_freudenthal_boundary_range(
    statement,
  )


def test_freudenthal_outside_range():
  statement = SuspensionMapStatement(
    sphere_dimension=5,
    stem=5,
  )

  assert not is_freudenthal_stable_range(
    statement,
  )

  assert not is_freudenthal_boundary_range(
    statement,
  )


def test_freudenthal_stable_range_implies_suspension_isomorphism():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  assert len(result) == 2

  assert result[1].conclusion == (
    SuspensionIsomorphismStatement(
      suspension_map=suspension_map,
    )
  )


def test_freudenthal_lower_stable_stem_implies_suspension_isomorphism():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  assert len(result) == 2

  assert result[1].conclusion == (
    SuspensionIsomorphismStatement(
      suspension_map=suspension_map,
    )
  )


def test_freudenthal_boundary_range_does_not_imply_suspension_isomorphism():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=4,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  assert result == (
    initial_step,
  )


def test_freudenthal_outside_range_does_not_imply_suspension_isomorphism():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=5,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  assert result == (
    initial_step,
  )


def test_freudenthal_suspension_isomorphism_preserves_provenance():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  derived_step = result[1]

  assert derived_step.conclusion == (
    SuspensionIsomorphismStatement(
      suspension_map=suspension_map,
    )
  )

  assert derived_step.premises == (
    initial_step,
  )

  assert (
    derived_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    derived_step.inference_rule
    == inference_rule
  )


def test_freudenthal_boundary_range_implies_suspension_epimorphism():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=4,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_boundary_epimorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  assert len(result) == 2

  assert result[1].conclusion == (
    SuspensionEpimorphismStatement(
      suspension_map=suspension_map,
    )
  )


def test_freudenthal_stable_range_does_not_use_boundary_epimorphism_rule():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_boundary_epimorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  assert result == (
    initial_step,
  )


def test_freudenthal_outside_range_does_not_imply_suspension_epimorphism():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=5,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_boundary_epimorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  assert result == (
    initial_step,
  )


def test_freudenthal_isomorphism_and_boundary_epimorphism_rules_do_not_overlap():
  stable_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  boundary_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=4,
  )

  stable_step = ProofStep(
    conclusion=stable_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  boundary_step = ProofStep(
    conclusion=boundary_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  isomorphism_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  epimorphism_rule = (
    freudenthal_boundary_epimorphism_inference_rule()
  )

  stable_isomorphism_result = (
    run_inference_round(
      isomorphism_rule,
      stable_step,
    )
  )

  stable_epimorphism_result = (
    run_inference_round(
      epimorphism_rule,
      stable_step,
    )
  )

  boundary_isomorphism_result = (
    run_inference_round(
      isomorphism_rule,
      boundary_step,
    )
  )

  boundary_epimorphism_result = (
    run_inference_round(
      epimorphism_rule,
      boundary_step,
    )
  )

  assert (
    stable_isomorphism_result[1].conclusion
    == SuspensionIsomorphismStatement(
      suspension_map=stable_map,
    )
  )

  assert stable_epimorphism_result == (
    stable_step,
  )

  assert boundary_isomorphism_result == (
    boundary_step,
  )

  assert (
    boundary_epimorphism_result[1].conclusion
    == SuspensionEpimorphismStatement(
      suspension_map=boundary_map,
    )
  )


def test_freudenthal_suspension_epimorphism_preserves_provenance():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=4,
  )

  initial_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    freudenthal_boundary_epimorphism_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    initial_step,
  )

  derived_step = result[1]

  assert derived_step.conclusion == (
    SuspensionEpimorphismStatement(
      suspension_map=suspension_map,
    )
  )

  assert derived_step.premises == (
    initial_step,
  )

  assert (
    derived_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    derived_step.inference_rule
    == inference_rule
  )


def test_suspension_isomorphism_implies_injective():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  isomorphism_step = ProofStep(
    conclusion=(
      SuspensionIsomorphismStatement(
        suspension_map=suspension_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    suspension_isomorphism_implies_injective_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    isomorphism_step,
  )

  assert len(result) == 2

  assert result[1].conclusion == (
    SuspensionInjectiveStatement(
      suspension_map=suspension_map,
    )
  )


def test_suspension_injectivity_preserves_provenance():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  isomorphism_step = ProofStep(
    conclusion=(
      SuspensionIsomorphismStatement(
        suspension_map=suspension_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    suspension_isomorphism_implies_injective_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    isomorphism_step,
  )

  injective_step = result[1]

  assert injective_step.premises == (
    isomorphism_step,
  )

  assert (
    injective_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    injective_step.inference_rule
    == inference_rule
  )


def test_suspension_injectivity_reflects_equality():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  lhs = eta(5)
  rhs = nu(5)

  injective_step = ProofStep(
    conclusion=(
      SuspensionInjectiveStatement(
        suspension_map=suspension_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_equality_step = ProofStep(
    conclusion=(
      SuspensionMapEqualityStatement(
        suspension_map=suspension_map,
        lhs=lhs,
        rhs=rhs,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    suspension_injectivity_reflects_equality_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    (
      injective_step,
      suspended_equality_step,
    ),
  )

  assert len(result) == 3

  assert result[2].conclusion == Relation(
    lhs=lhs,
    rhs=rhs,
    relation_type=RelationType.EQUALITY,
  )


def test_suspension_injectivity_does_not_reflect_equality_from_different_map():
  injective_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  equality_map = SuspensionMapStatement(
    sphere_dimension=6,
    stem=3,
  )

  lhs = eta(5)
  rhs = nu(5)

  injective_step = ProofStep(
    conclusion=(
      SuspensionInjectiveStatement(
        suspension_map=injective_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_equality_step = ProofStep(
    conclusion=(
      SuspensionMapEqualityStatement(
        suspension_map=equality_map,
        lhs=lhs,
        rhs=rhs,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    suspension_injectivity_reflects_equality_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    (
      injective_step,
      suspended_equality_step,
    ),
  )

  assert result == (
    injective_step,
    suspended_equality_step,
  )


def test_suspension_equality_reflection_preserves_provenance():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  lhs = eta(5)
  rhs = nu(5)

  injective_step = ProofStep(
    conclusion=(
      SuspensionInjectiveStatement(
        suspension_map=suspension_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_equality_step = ProofStep(
    conclusion=(
      SuspensionMapEqualityStatement(
        suspension_map=suspension_map,
        lhs=lhs,
        rhs=rhs,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    suspension_injectivity_reflects_equality_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    (
      injective_step,
      suspended_equality_step,
    ),
  )

  reflected_step = result[2]

  assert reflected_step.conclusion == Relation(
    lhs=lhs,
    rhs=rhs,
    relation_type=RelationType.EQUALITY,
  )

  assert reflected_step.premises == (
    injective_step,
    suspended_equality_step,
  )

  assert (
    reflected_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    reflected_step.inference_rule
    == inference_rule
  )


def test_suspension_injectivity_reflects_zero():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  element = eta(5)

  injective_step = ProofStep(
    conclusion=(
      SuspensionInjectiveStatement(
        suspension_map=suspension_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_zero_step = ProofStep(
    conclusion=(
      SuspensionMapZeroStatement(
        suspension_map=suspension_map,
        expression=element,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    suspension_injectivity_reflects_zero_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    (
      injective_step,
      suspended_zero_step,
    ),
  )

  assert len(result) == 3

  assert result[2].conclusion == Relation(
    lhs=element,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )


def test_suspension_injectivity_does_not_reflect_zero_from_different_map():
  injective_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  zero_map = SuspensionMapStatement(
    sphere_dimension=6,
    stem=3,
  )

  element = eta(5)

  injective_step = ProofStep(
    conclusion=(
      SuspensionInjectiveStatement(
        suspension_map=injective_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_zero_step = ProofStep(
    conclusion=(
      SuspensionMapZeroStatement(
        suspension_map=zero_map,
        expression=element,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    suspension_injectivity_reflects_zero_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    (
      injective_step,
      suspended_zero_step,
    ),
  )

  assert result == (
    injective_step,
    suspended_zero_step,
  )


def test_suspension_zero_reflection_preserves_provenance():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  element = eta(5)

  injective_step = ProofStep(
    conclusion=(
      SuspensionInjectiveStatement(
        suspension_map=suspension_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_zero_step = ProofStep(
    conclusion=(
      SuspensionMapZeroStatement(
        suspension_map=suspension_map,
        expression=element,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  inference_rule = (
    suspension_injectivity_reflects_zero_inference_rule()
  )

  result = run_inference_round(
    inference_rule,
    (
      injective_step,
      suspended_zero_step,
    ),
  )

  reflected_step = result[2]

  assert reflected_step.conclusion == Relation(
    lhs=element,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert reflected_step.premises == (
    injective_step,
    suspended_zero_step,
  )

  assert (
    reflected_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    reflected_step.inference_rule
    == inference_rule
  )


def test_freudenthal_isomorphism_reaches_injectivity_over_two_rounds():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  map_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  isomorphism_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  injectivity_rule = (
    suspension_isomorphism_implies_injective_inference_rule()
  )

  first_round = run_inference_round(
    isomorphism_rule,
    map_step,
  )

  assert first_round[1].conclusion == (
    SuspensionIsomorphismStatement(
      suspension_map=suspension_map,
    )
  )

  second_round = run_inference_round(
    injectivity_rule,
    first_round,
  )

  assert second_round[2].conclusion == (
    SuspensionInjectiveStatement(
      suspension_map=suspension_map,
    )
  )

  assert second_round[2].premises == (
    first_round[1],
  )


def test_freudenthal_stable_range_reaches_zero_reflection_over_fixed_point():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  element = eta(5)

  map_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_zero_step = ProofStep(
    conclusion=(
      SuspensionMapZeroStatement(
        suspension_map=suspension_map,
        expression=element,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  isomorphism_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  injectivity_rule = (
    suspension_isomorphism_implies_injective_inference_rule()
  )

  zero_reflection_rule = (
    suspension_injectivity_reflects_zero_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        isomorphism_rule,
        injectivity_rule,
        zero_reflection_rule,
      ),
      (
        map_step,
        suspended_zero_step,
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3

  assert len(result.round_history) == 3

  isomorphism_step = (
    result.round_history[0][0]
  )

  injective_step = (
    result.round_history[1][0]
  )

  reflected_zero_step = (
    result.round_history[2][0]
  )

  assert isomorphism_step.conclusion == (
    SuspensionIsomorphismStatement(
      suspension_map=suspension_map,
    )
  )

  assert isomorphism_step.premises == (
    map_step,
  )

  assert (
    isomorphism_step.inference_rule
    == isomorphism_rule
  )

  assert injective_step.conclusion == (
    SuspensionInjectiveStatement(
      suspension_map=suspension_map,
    )
  )

  assert injective_step.premises == (
    isomorphism_step,
  )

  assert (
    injective_step.inference_rule
    == injectivity_rule
  )

  assert reflected_zero_step.conclusion == Relation(
    lhs=element,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert reflected_zero_step.premises == (
    injective_step,
    suspended_zero_step,
  )

  assert (
    reflected_zero_step.inference_rule
    == zero_reflection_rule
  )

  assert (
    reflected_zero_step
    in result.steps
  )


def test_phase9_representative_stable_reflection_generic_reasoning_scenario_reaches_fixed_point():
  suspension_map = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  left_element = eta(5)
  right_element = nu(5)

  map_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_equality_step = ProofStep(
    conclusion=(
      SuspensionMapEqualityStatement(
        suspension_map=suspension_map,
        lhs=left_element,
        rhs=right_element,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_zero_step = ProofStep(
    conclusion=(
      SuspensionMapZeroStatement(
        suspension_map=suspension_map,
        expression=left_element,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  isomorphism_rule = (
    freudenthal_stable_isomorphism_inference_rule()
  )

  injectivity_rule = (
    suspension_isomorphism_implies_injective_inference_rule()
  )

  equality_reflection_rule = (
    suspension_injectivity_reflects_equality_inference_rule()
  )

  zero_reflection_rule = (
    suspension_injectivity_reflects_zero_inference_rule()
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  zero_propagation_rule = (
    zero_equality_implies_zero_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        isomorphism_rule,
        injectivity_rule,
        equality_reflection_rule,
        zero_reflection_rule,
        symmetry_rule,
        transitivity_rule,
        zero_propagation_rule,
      ),
      (
        map_step,
        suspended_equality_step,
        suspended_zero_step,
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 5

  isomorphism_conclusion = (
    SuspensionIsomorphismStatement(
      suspension_map=suspension_map,
    )
  )

  injective_conclusion = (
    SuspensionInjectiveStatement(
      suspension_map=suspension_map,
    )
  )

  reflected_equality = Relation(
    lhs=left_element,
    rhs=right_element,
    relation_type=RelationType.EQUALITY,
  )

  reflected_zero = Relation(
    lhs=left_element,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  symmetric_equality = Relation(
    lhs=right_element,
    rhs=left_element,
    relation_type=RelationType.EQUALITY,
  )

  propagated_zero = Relation(
    lhs=right_element,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert any(
    step.conclusion
    == isomorphism_conclusion
    for step in result.steps
  )

  assert any(
    step.conclusion
    == injective_conclusion
    for step in result.steps
  )

  assert any(
    step.conclusion
    == reflected_equality
    for step in result.steps
  )

  assert any(
    step.conclusion
    == reflected_zero
    for step in result.steps
  )

  assert any(
    step.conclusion
    == symmetric_equality
    for step in result.steps
  )

  assert any(
    step.conclusion
    == propagated_zero
    for step in result.steps
  )

  isomorphism_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == isomorphism_conclusion
    )
  )

  injective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == injective_conclusion
    )
  )

  reflected_equality_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == reflected_equality
    )
  )

  reflected_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == reflected_zero
    )
  )

  symmetric_equality_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == symmetric_equality
    )
  )

  propagated_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == propagated_zero
    )
  )

  assert isomorphism_step.premises == (
    map_step,
  )

  assert (
    isomorphism_step.inference_rule
    == isomorphism_rule
  )

  assert injective_step.premises == (
    isomorphism_step,
  )

  assert (
    injective_step.inference_rule
    == injectivity_rule
  )

  assert reflected_equality_step.premises == (
    injective_step,
    suspended_equality_step,
  )

  assert (
    reflected_equality_step.inference_rule
    == equality_reflection_rule
  )

  assert reflected_zero_step.premises == (
    injective_step,
    suspended_zero_step,
  )

  assert (
    reflected_zero_step.inference_rule
    == zero_reflection_rule
  )

  assert symmetric_equality_step.premises == (
    reflected_equality_step,
  )

  assert (
    symmetric_equality_step.inference_rule
    == symmetry_rule
  )

  assert propagated_zero_step.premises == (
    reflected_zero_step,
    symmetric_equality_step,
  )

  assert (
    propagated_zero_step.inference_rule
    == zero_propagation_rule
  )

  assert (
    isomorphism_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    injective_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    reflected_equality_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    reflected_zero_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    symmetric_equality_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    propagated_zero_step.rule
    == ProofRule.INFERENCE
  )










