from proof import (
  ProofRule,
  ProofStep,
  run_inference_round,
)
from stable_rules import (
  SuspensionIsomorphismStatement,
  SuspensionMapStatement,
  freudenthal_stable_isomorphism_inference_rule,
  is_freudenthal_boundary_range,
  is_freudenthal_stable_range,
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








