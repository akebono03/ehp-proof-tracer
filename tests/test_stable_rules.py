from expression import (
  Zero,
  eta,
  nu,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_round,
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






